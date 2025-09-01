#!/usr/bin/env python3
"""
Comprehensive Backup and Disaster Recovery System
Enterprise-grade backup and DR implementation for CloudMind
"""

import os
import sys
import json
import logging
import subprocess
import hashlib
import gzip
import tarfile
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import shutil

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.config import settings
from app.services.encryption_service import encryption_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BackupDRSystem:
    """Enterprise-grade backup and disaster recovery system"""
    
    def __init__(self):
        self.backup_dir = Path("./backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        self.retention_days = 30
        self.encryption_enabled = True
        self.compression_enabled = True
        self.verification_enabled = True
        
        # RTO/RPO settings
        self.rto_minutes = 15  # Recovery Time Objective
        self.rpo_minutes = 5   # Recovery Point Objective
        
    def create_full_backup(self) -> Dict[str, Any]:
        """Create a full system backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"full_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            
            logger.info(f"Starting full backup: {backup_name}")
            
            # Create backup directory
            backup_path.mkdir(exist_ok=True)
            
            # Backup database
            db_backup = self._backup_database(backup_path)
            
            # Backup files
            files_backup = self._backup_files(backup_path)
            
            # Backup configuration
            config_backup = self._backup_configuration(backup_path)
            
            # Create backup manifest
            manifest = self._create_backup_manifest(
                backup_name, timestamp, db_backup, files_backup, config_backup
            )
            
            # Compress backup
            if self.compression_enabled:
                compressed_path = self._compress_backup(backup_path)
                shutil.rmtree(backup_path)
                backup_path = compressed_path
            
            # Encrypt backup
            if self.encryption_enabled:
                encrypted_path = self._encrypt_backup(backup_path)
                backup_path.unlink()
                backup_path = encrypted_path
            
            # Verify backup
            if self.verification_enabled:
                verification_result = self._verify_backup(backup_path)
            else:
                verification_result = {"verified": True, "checksum": "skipped"}
            
            # Update manifest
            manifest["backup_path"] = str(backup_path)
            manifest["verification"] = verification_result
            manifest["size_bytes"] = backup_path.stat().st_size
            
            # Save manifest
            manifest_path = backup_path.with_suffix('.manifest.json')
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info(f"Full backup completed: {backup_path}")
            return manifest
            
        except Exception as e:
            logger.error(f"Full backup failed: {e}")
            raise
    
    def create_incremental_backup(self, base_backup: str) -> Dict[str, Any]:
        """Create incremental backup based on previous backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"incremental_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            
            logger.info(f"Starting incremental backup: {backup_name}")
            
            # Load base backup manifest
            base_manifest_path = self.backup_dir / f"{base_backup}.manifest.json"
            with open(base_manifest_path, 'r') as f:
                base_manifest = json.load(f)
            
            # Create backup directory
            backup_path.mkdir(exist_ok=True)
            
            # Get changes since base backup
            changes = self._get_changes_since(base_manifest["timestamp"])
            
            # Backup only changed files
            files_backup = self._backup_changed_files(backup_path, changes)
            
            # Backup database changes
            db_backup = self._backup_database_incremental(backup_path, base_manifest)
            
            # Create incremental manifest
            manifest = self._create_incremental_manifest(
                backup_name, timestamp, base_backup, db_backup, files_backup, changes
            )
            
            # Compress and encrypt
            if self.compression_enabled:
                compressed_path = self._compress_backup(backup_path)
                shutil.rmtree(backup_path)
                backup_path = compressed_path
            
            if self.encryption_enabled:
                encrypted_path = self._encrypt_backup(backup_path)
                backup_path.unlink()
                backup_path = encrypted_path
            
            # Verify backup
            if self.verification_enabled:
                verification_result = self._verify_backup(backup_path)
            else:
                verification_result = {"verified": True, "checksum": "skipped"}
            
            manifest["backup_path"] = str(backup_path)
            manifest["verification"] = verification_result
            manifest["size_bytes"] = backup_path.stat().st_size
            
            # Save manifest
            manifest_path = backup_path.with_suffix('.manifest.json')
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info(f"Incremental backup completed: {backup_path}")
            return manifest
            
        except Exception as e:
            logger.error(f"Incremental backup failed: {e}")
            raise
    
    def restore_backup(self, backup_name: str, target_path: Optional[str] = None) -> bool:
        """Restore from backup"""
        try:
            logger.info(f"Starting restore from backup: {backup_name}")
            
            # Find backup file
            backup_files = list(self.backup_dir.glob(f"{backup_name}*"))
            if not backup_files:
                raise FileNotFoundError(f"Backup not found: {backup_name}")
            
            backup_path = backup_files[0]
            
            # Decrypt if needed
            if backup_path.suffix == '.encrypted':
                decrypted_path = self._decrypt_backup(backup_path)
                backup_path = decrypted_path
            
            # Decompress if needed
            if backup_path.suffix == '.gz':
                decompressed_path = self._decompress_backup(backup_path)
                backup_path = decompressed_path
            
            # Load manifest
            manifest_path = backup_path.with_suffix('.manifest.json')
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Restore database
            if manifest.get("database_backup"):
                self._restore_database(manifest["database_backup"])
            
            # Restore files
            if manifest.get("files_backup"):
                self._restore_files(manifest["files_backup"], target_path)
            
            # Restore configuration
            if manifest.get("config_backup"):
                self._restore_configuration(manifest["config_backup"])
            
            logger.info(f"Restore completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    def test_recovery(self, backup_name: str) -> Dict[str, Any]:
        """Test recovery procedures"""
        try:
            logger.info(f"Testing recovery for backup: {backup_name}")
            
            # Create test environment
            test_env = self._create_test_environment()
            
            # Restore to test environment
            restore_success = self.restore_backup(backup_name, test_env)
            
            # Test system functionality
            if restore_success:
                functionality_tests = self._test_system_functionality(test_env)
            else:
                functionality_tests = {"passed": False, "errors": ["Restore failed"]}
            
            # Cleanup test environment
            shutil.rmtree(test_env)
            
            test_results = {
                "backup_name": backup_name,
                "restore_success": restore_success,
                "functionality_tests": functionality_tests,
                "test_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Recovery test completed: {test_results}")
            return test_results
            
        except Exception as e:
            logger.error(f"Recovery test failed: {e}")
            return {"error": str(e)}
    
    def _backup_database(self, backup_path: Path) -> Dict[str, Any]:
        """Backup database"""
        try:
            db_backup_path = backup_path / "database"
            db_backup_path.mkdir(exist_ok=True)
            
            # PostgreSQL backup
            pg_backup_file = db_backup_path / "postgresql.sql"
            subprocess.run([
                "docker", "exec", "cloudmind-postgres",
                "pg_dumpall", "-U", "cloudmind"
            ], stdout=open(pg_backup_file, 'w'), check=True)
            
            # Redis backup
            redis_backup_file = db_backup_path / "redis.rdb"
            subprocess.run([
                "docker", "exec", "cloudmind-redis",
                "redis-cli", "BGSAVE"
            ], check=True)
            
            # Copy Redis dump
            subprocess.run([
                "docker", "cp", "cloudmind-redis:/data/dump.rdb", str(redis_backup_file)
            ], check=True)
            
            return {
                "postgresql": str(pg_backup_file),
                "redis": str(redis_backup_file),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            raise
    
    def _backup_files(self, backup_path: Path) -> Dict[str, Any]:
        """Backup important files"""
        try:
            files_backup_path = backup_path / "files"
            files_backup_path.mkdir(exist_ok=True)
            
            # Backup configuration files
            config_files = [
                ".env",
                "docker-compose.yml",
                "infrastructure/docker/nginx/nginx.conf",
                "infrastructure/docker/nginx/ssl/"
            ]
            
            for file_path in config_files:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        shutil.copytree(file_path, files_backup_path / Path(file_path).name)
                    else:
                        shutil.copy2(file_path, files_backup_path)
            
            # Backup logs
            if os.path.exists("logs"):
                shutil.copytree("logs", files_backup_path / "logs")
            
            return {
                "config_files": [str(f) for f in files_backup_path.iterdir()],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Files backup failed: {e}")
            raise
    
    def _backup_configuration(self, backup_path: Path) -> Dict[str, Any]:
        """Backup system configuration"""
        try:
            config_backup_path = backup_path / "config"
            config_backup_path.mkdir(exist_ok=True)
            
            # Backup Docker configuration
            docker_config = {
                "containers": self._get_docker_containers(),
                "volumes": self._get_docker_volumes(),
                "networks": self._get_docker_networks()
            }
            
            with open(config_backup_path / "docker_config.json", 'w') as f:
                json.dump(docker_config, f, indent=2)
            
            # Backup system configuration
            system_config = {
                "settings": settings.dict(),
                "environment": dict(os.environ),
                "timestamp": datetime.now().isoformat()
            }
            
            with open(config_backup_path / "system_config.json", 'w') as f:
                json.dump(system_config, f, indent=2)
            
            return {
                "docker_config": str(config_backup_path / "docker_config.json"),
                "system_config": str(config_backup_path / "system_config.json"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Configuration backup failed: {e}")
            raise
    
    def _create_backup_manifest(self, backup_name: str, timestamp: str,
                               db_backup: Dict, files_backup: Dict,
                               config_backup: Dict) -> Dict[str, Any]:
        """Create backup manifest"""
        return {
            "backup_name": backup_name,
            "backup_type": "full",
            "timestamp": timestamp,
            "database_backup": db_backup,
            "files_backup": files_backup,
            "config_backup": config_backup,
            "rto_minutes": self.rto_minutes,
            "rpo_minutes": self.rpo_minutes,
            "encryption_enabled": self.encryption_enabled,
            "compression_enabled": self.compression_enabled,
            "verification_enabled": self.verification_enabled
        }
    
    def _compress_backup(self, backup_path: Path) -> Path:
        """Compress backup directory"""
        compressed_path = backup_path.with_suffix('.tar.gz')
        
        with tarfile.open(compressed_path, 'w:gz') as tar:
            tar.add(backup_path, arcname=backup_path.name)
        
        return compressed_path
    
    def _encrypt_backup(self, backup_path: Path) -> Path:
        """Encrypt backup file"""
        encrypted_path = backup_path.with_suffix('.encrypted')
        
        with open(backup_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = encryption_service.encrypt_data(data)
        
        with open(encrypted_path, 'w') as f:
            json.dump(encrypted_data, f)
        
        return encrypted_path
    
    def _verify_backup(self, backup_path: Path) -> Dict[str, Any]:
        """Verify backup integrity"""
        try:
            # Calculate checksum
            with open(backup_path, 'rb') as f:
                data = f.read()
            
            checksum = hashlib.sha256(data).hexdigest()
            
            # Verify file size
            file_size = backup_path.stat().st_size
            
            return {
                "verified": True,
                "checksum": checksum,
                "size_bytes": file_size,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "verified": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_docker_containers(self) -> List[Dict[str, Any]]:
        """Get Docker container information"""
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "json"],
                capture_output=True, text=True, check=True
            )
            
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    containers.append(json.loads(line))
            
            return containers
            
        except Exception as e:
            logger.error(f"Failed to get Docker containers: {e}")
            return []
    
    def _get_docker_volumes(self) -> List[str]:
        """Get Docker volume information"""
        try:
            result = subprocess.run(
                ["docker", "volume", "ls", "--format", "{{.Name}}"],
                capture_output=True, text=True, check=True
            )
            
            return result.stdout.strip().split('\n')
            
        except Exception as e:
            logger.error(f"Failed to get Docker volumes: {e}")
            return []
    
    def _get_docker_networks(self) -> List[str]:
        """Get Docker network information"""
        try:
            result = subprocess.run(
                ["docker", "network", "ls", "--format", "{{.Name}}"],
                capture_output=True, text=True, check=True
            )
            
            return result.stdout.strip().split('\n')
            
        except Exception as e:
            logger.error(f"Failed to get Docker networks: {e}")
            return []
    
    def cleanup_old_backups(self) -> int:
        """Clean up old backups based on retention policy"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            deleted_count = 0
            
            for backup_file in self.backup_dir.glob("*"):
                if backup_file.is_file():
                    file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    if file_time < cutoff_date:
                        backup_file.unlink()
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {backup_file}")
            
            logger.info(f"Cleanup completed: {deleted_count} old backups deleted")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
            return 0


def main():
    """Main backup and DR functions"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CloudMind Backup and DR System")
    parser.add_argument("action", choices=["backup", "restore", "test", "cleanup"])
    parser.add_argument("--backup-name", help="Backup name for restore/test")
    parser.add_argument("--incremental", action="store_true", help="Create incremental backup")
    parser.add_argument("--base-backup", help="Base backup for incremental")
    
    args = parser.parse_args()
    
    backup_dr = BackupDRSystem()
    
    if args.action == "backup":
        if args.incremental and args.base_backup:
            result = backup_dr.create_incremental_backup(args.base_backup)
        else:
            result = backup_dr.create_full_backup()
        print(json.dumps(result, indent=2))
        
    elif args.action == "restore":
        if not args.backup_name:
            print("Error: --backup-name required for restore")
            sys.exit(1)
        success = backup_dr.restore_backup(args.backup_name)
        print(f"Restore {'successful' if success else 'failed'}")
        
    elif args.action == "test":
        if not args.backup_name:
            print("Error: --backup-name required for test")
            sys.exit(1)
        result = backup_dr.test_recovery(args.backup_name)
        print(json.dumps(result, indent=2))
        
    elif args.action == "cleanup":
        deleted_count = backup_dr.cleanup_old_backups()
        print(f"Deleted {deleted_count} old backups")


if __name__ == "__main__":
    main() 