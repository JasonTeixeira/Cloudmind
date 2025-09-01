"""
Advanced Extension Marketplace Service
Professional marketplace for extension discovery, search, and management
"""

import asyncio
import logging
import os
import json
import requests
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple, Union
from uuid import UUID, uuid4
from pathlib import Path
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

from app.core.config import settings
from app.schemas.extension import (
    Extension, ExtensionMarketplace, ExtensionReview, ExtensionUpdate,
    ExtensionCategory, ExtensionType, ExtensionRating, ExtensionCompatibility,
    ExtensionStatus, SearchExtensionsRequest, SearchExtensionsResponse
)

logger = logging.getLogger(__name__)


class MarketplaceService:
    """Manages extension marketplace operations"""
    
    def __init__(self):
        self.marketplaces: Dict[str, ExtensionMarketplace] = {}
        self.extensions: Dict[str, Extension] = {}
        self.reviews: Dict[str, List[ExtensionReview]] = {}
        self.updates: Dict[str, List[ExtensionUpdate]] = {}
        self.cache: Dict[str, Any] = {}
        self.cache_expiry: Dict[str, datetime] = {}
        
        # Initialize default marketplace
        self._initialize_default_marketplace()
        
    def _initialize_default_marketplace(self):
        """Initialize default marketplace"""
        default_marketplace = ExtensionMarketplace(
            id="cloudmind-official",
            name="CloudMind Official Marketplace",
            description="Official CloudMind extension marketplace",
            url="https://marketplace.cloudmind.dev",
            api_url="https://api.marketplace.cloudmind.dev",
            is_official=True,
            is_enabled=True,
            extension_count=0,
            sync_interval=3600
        )
        
        self.marketplaces[default_marketplace.id] = default_marketplace
        
        # Add some sample extensions
        self._add_sample_extensions()
    
    def _add_sample_extensions(self):
        """Add sample extensions for demonstration"""
        sample_extensions = [
            Extension(
                id="python-language-support",
                name="python-language-support",
                display_name="Python Language Support",
                description="Enhanced Python language support with syntax highlighting, linting, and debugging",
                version="1.0.0",
                author="CloudMind Team",
                publisher="cloudmind",
                type=ExtensionType.LANGUAGE,
                category=ExtensionCategory.PROGRAMMING_LANGUAGES,
                status=ExtensionStatus.UNINSTALLED,
                icon_url="https://example.com/python-icon.png",
                repository_url="https://github.com/cloudmind/python-support",
                homepage_url="https://python.cloudmind.dev",
                license="MIT",
                tags=["python", "language", "syntax", "linting"],
                permissions=[
                    "read_files",
                    "write_files",
                    "access_debugger"
                ],
                dependencies=[],
                conflicts=[],
                compatibility=ExtensionCompatibility.COMPATIBLE,
                rating=ExtensionRating.EXCELLENT,
                download_count=1500,
                review_count=45,
                average_rating=4.8,
                size=2048576,
                is_verified=True,
                is_featured=True
            ),
            Extension(
                id="dark-theme-pro",
                name="dark-theme-pro",
                display_name="Dark Theme Pro",
                description="Professional dark theme with customizable colors and syntax highlighting",
                version="2.1.0",
                author="Theme Studio",
                publisher="themestudio",
                type=ExtensionType.THEME,
                category=ExtensionCategory.THEMES,
                status=ExtensionStatus.UNINSTALLED,
                icon_url="https://example.com/dark-theme-icon.png",
                repository_url="https://github.com/themestudio/dark-theme-pro",
                homepage_url="https://darktheme.themestudio.dev",
                license="MIT",
                tags=["theme", "dark", "colors", "syntax"],
                permissions=[
                    "modify_ui"
                ],
                dependencies=[],
                conflicts=[],
                compatibility=ExtensionCompatibility.COMPATIBLE,
                rating=ExtensionRating.GOOD,
                download_count=3200,
                review_count=128,
                average_rating=4.5,
                size=512000,
                is_verified=True,
                is_featured=False
            ),
            Extension(
                id="git-integration",
                name="git-integration",
                display_name="Git Integration",
                description="Advanced Git integration with visual diff, branch management, and commit history",
                version="1.5.2",
                author="Git Tools Inc",
                publisher="gittools",
                type=ExtensionType.GIT,
                category=ExtensionCategory.VERSION_CONTROL,
                status=ExtensionStatus.UNINSTALLED,
                icon_url="https://example.com/git-icon.png",
                repository_url="https://github.com/gittools/git-integration",
                homepage_url="https://git.gittools.dev",
                license="Apache-2.0",
                tags=["git", "version-control", "diff", "branch"],
                permissions=[
                    "read_files",
                    "write_files",
                    "execute_commands",
                    "access_terminal"
                ],
                dependencies=[],
                conflicts=[],
                compatibility=ExtensionCompatibility.COMPATIBLE,
                rating=ExtensionRating.EXCELLENT,
                download_count=8900,
                review_count=234,
                average_rating=4.9,
                size=1536000,
                is_verified=True,
                is_featured=True
            ),
            Extension(
                id="code-snippets",
                name="code-snippets",
                display_name="Code Snippets",
                description="Extensive collection of code snippets for multiple programming languages",
                version="3.0.1",
                author="Snippet Library",
                publisher="snippetlib",
                type=ExtensionType.SNIPPET,
                category=ExtensionCategory.SNIPPETS,
                status=ExtensionStatus.UNINSTALLED,
                icon_url="https://example.com/snippets-icon.png",
                repository_url="https://github.com/snippetlib/code-snippets",
                homepage_url="https://snippets.snippetlib.dev",
                license="MIT",
                tags=["snippets", "code", "templates", "productivity"],
                permissions=[
                    "read_files",
                    "write_files"
                ],
                dependencies=[],
                conflicts=[],
                compatibility=ExtensionCompatibility.COMPATIBLE,
                rating=ExtensionRating.GOOD,
                download_count=5600,
                review_count=89,
                average_rating=4.3,
                size=3072000,
                is_verified=True,
                is_featured=False
            ),
            Extension(
                id="database-explorer",
                name="database-explorer",
                display_name="Database Explorer",
                description="Visual database explorer with query builder and data visualization",
                version="1.2.0",
                author="DB Tools",
                publisher="dbtools",
                type=ExtensionType.DATABASE,
                category=ExtensionCategory.DATABASES,
                status=ExtensionStatus.UNINSTALLED,
                icon_url="https://example.com/database-icon.png",
                repository_url="https://github.com/dbtools/database-explorer",
                homepage_url="https://db.dbtools.dev",
                license="GPL-3.0",
                tags=["database", "sql", "query", "visualization"],
                permissions=[
                    "access_database",
                    "read_files",
                    "write_files"
                ],
                dependencies=[],
                conflicts=[],
                compatibility=ExtensionCompatibility.COMPATIBLE,
                rating=ExtensionRating.GOOD,
                download_count=2100,
                review_count=67,
                average_rating=4.4,
                size=2048000,
                is_verified=True,
                is_featured=False
            )
        ]
        
        for extension in sample_extensions:
            self.extensions[extension.id] = extension
    
    async def search_extensions(self, request: SearchExtensionsRequest) -> SearchExtensionsResponse:
        """Search extensions in marketplace"""
        try:
            # Get all extensions
            all_extensions = list(self.extensions.values())
            
            # Apply filters
            filtered_extensions = []
            
            for extension in all_extensions:
                # Query filter
                if request.query.lower() not in extension.name.lower() and \
                   request.query.lower() not in extension.display_name.lower() and \
                   request.query.lower() not in extension.description.lower():
                    continue
                
                # Category filter
                if request.category and extension.category != request.category:
                    continue
                
                # Type filter
                if request.type and extension.type != request.type:
                    continue
                
                # Rating filter
                if request.rating and extension.rating != request.rating:
                    continue
                
                # Verified filter
                if request.is_verified is not None and extension.is_verified != request.is_verified:
                    continue
                
                # Featured filter
                if request.is_featured is not None and extension.is_featured != request.is_featured:
                    continue
                
                filtered_extensions.append(extension)
            
            # Apply sorting
            if request.sort_by == "name":
                filtered_extensions.sort(key=lambda x: x.display_name)
            elif request.sort_by == "downloads":
                filtered_extensions.sort(key=lambda x: x.download_count, reverse=True)
            elif request.sort_by == "rating":
                filtered_extensions.sort(key=lambda x: x.average_rating, reverse=True)
            elif request.sort_by == "updated":
                filtered_extensions.sort(key=lambda x: x.updated_at or x.installed_at, reverse=True)
            else:  # relevance
                # Sort by relevance (featured first, then by rating and downloads)
                filtered_extensions.sort(key=lambda x: (
                    not x.is_featured,
                    -x.average_rating,
                    -x.download_count
                ))
            
            # Apply reverse order if needed
            if request.sort_order == "asc":
                filtered_extensions.reverse()
            
            # Apply pagination
            start_idx = (request.page - 1) * request.page_size
            end_idx = start_idx + request.page_size
            paginated_extensions = filtered_extensions[start_idx:end_idx]
            
            return SearchExtensionsResponse(
                extensions=paginated_extensions,
                total_count=len(filtered_extensions),
                page=request.page,
                page_size=request.page_size,
                has_more=end_idx < len(filtered_extensions)
            )
            
        except Exception as e:
            logger.error(f"Failed to search extensions: {e}")
            return SearchExtensionsResponse(
                extensions=[],
                total_count=0,
                page=request.page,
                page_size=request.page_size,
                has_more=False
            )
    
    async def get_extension_details(self, extension_id: str) -> Optional[Extension]:
        """Get extension details"""
        try:
            return self.extensions.get(extension_id)
            
        except Exception as e:
            logger.error(f"Failed to get extension details for {extension_id}: {e}")
            return None
    
    async def get_featured_extensions(self, limit: int = 10) -> List[Extension]:
        """Get featured extensions"""
        try:
            featured = [
                ext for ext in self.extensions.values()
                if ext.is_featured
            ]
            
            # Sort by rating and downloads
            featured.sort(key=lambda x: (x.average_rating, x.download_count), reverse=True)
            
            return featured[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get featured extensions: {e}")
            return []
    
    async def get_popular_extensions(self, limit: int = 10) -> List[Extension]:
        """Get popular extensions"""
        try:
            popular = list(self.extensions.values())
            
            # Sort by download count
            popular.sort(key=lambda x: x.download_count, reverse=True)
            
            return popular[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get popular extensions: {e}")
            return []
    
    async def get_extensions_by_category(
        self, 
        category: ExtensionCategory, 
        limit: int = 20
    ) -> List[Extension]:
        """Get extensions by category"""
        try:
            category_extensions = [
                ext for ext in self.extensions.values()
                if ext.category == category
            ]
            
            # Sort by rating and downloads
            category_extensions.sort(key=lambda x: (x.average_rating, x.download_count), reverse=True)
            
            return category_extensions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get extensions by category {category}: {e}")
            return []
    
    async def get_extensions_by_type(
        self, 
        extension_type: ExtensionType, 
        limit: int = 20
    ) -> List[Extension]:
        """Get extensions by type"""
        try:
            type_extensions = [
                ext for ext in self.extensions.values()
                if ext.type == extension_type
            ]
            
            # Sort by rating and downloads
            type_extensions.sort(key=lambda x: (x.average_rating, x.download_count), reverse=True)
            
            return type_extensions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get extensions by type {extension_type}: {e}")
            return []
    
    async def get_extension_reviews(
        self, 
        extension_id: str, 
        limit: int = 20
    ) -> List[ExtensionReview]:
        """Get extension reviews"""
        try:
            reviews = self.reviews.get(extension_id, [])
            
            # Sort by creation date
            reviews.sort(key=lambda x: x.created_at, reverse=True)
            
            return reviews[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get reviews for extension {extension_id}: {e}")
            return []
    
    async def add_extension_review(
        self, 
        extension_id: str, 
        user_id: UUID,
        rating: int,
        title: str,
        content: str
    ) -> ExtensionReview:
        """Add extension review"""
        try:
            review = ExtensionReview(
                id=str(uuid4()),
                extension_id=extension_id,
                user_id=user_id,
                rating=rating,
                title=title,
                content=content,
                created_at=datetime.utcnow()
            )
            
            if extension_id not in self.reviews:
                self.reviews[extension_id] = []
            
            self.reviews[extension_id].append(review)
            
            # Update extension statistics
            if extension_id in self.extensions:
                extension = self.extensions[extension_id]
                extension.review_count += 1
                
                # Recalculate average rating
                all_reviews = self.reviews[extension_id]
                if all_reviews:
                    total_rating = sum(r.rating for r in all_reviews)
                    extension.average_rating = total_rating / len(all_reviews)
                    
                    # Update rating category
                    if extension.average_rating >= 4.5:
                        extension.rating = ExtensionRating.EXCELLENT
                    elif extension.average_rating >= 4.0:
                        extension.rating = ExtensionRating.GOOD
                    elif extension.average_rating >= 3.0:
                        extension.rating = ExtensionRating.AVERAGE
                    else:
                        extension.rating = ExtensionRating.POOR
            
            logger.info(f"Review added for extension {extension_id} by user {user_id}")
            return review
            
        except Exception as e:
            logger.error(f"Failed to add review for extension {extension_id}: {e}")
            raise
    
    async def get_extension_updates(
        self, 
        extension_id: str, 
        current_version: str
    ) -> List[ExtensionUpdate]:
        """Get available updates for extension"""
        try:
            updates = self.updates.get(extension_id, [])
            
            # Filter updates newer than current version
            available_updates = [
                update for update in updates
                if self._compare_versions(update.new_version, current_version) > 0
            ]
            
            # Sort by version
            available_updates.sort(key=lambda x: x.new_version, reverse=True)
            
            return available_updates
            
        except Exception as e:
            logger.error(f"Failed to get updates for extension {extension_id}: {e}")
            return []
    
    async def sync_marketplace(self, marketplace_id: str) -> bool:
        """Sync marketplace with external source"""
        try:
            marketplace = self.marketplaces.get(marketplace_id)
            if not marketplace:
                raise ValueError(f"Marketplace {marketplace_id} not found")
            
            # This is a simplified implementation
            # In a real implementation, you would sync with external APIs
            
            # Update sync time
            marketplace.last_sync = datetime.utcnow()
            marketplace.extension_count = len(self.extensions)
            
            logger.info(f"Marketplace {marketplace_id} synced successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync marketplace {marketplace_id}: {e}")
            return False
    
    async def get_marketplace_statistics(self) -> Dict[str, Any]:
        """Get marketplace statistics"""
        try:
            total_extensions = len(self.extensions)
            total_reviews = sum(len(reviews) for reviews in self.reviews.values())
            total_downloads = sum(ext.download_count for ext in self.extensions.values())
            
            # Category distribution
            category_distribution = {}
            for ext in self.extensions.values():
                category = ext.category.value
                category_distribution[category] = category_distribution.get(category, 0) + 1
            
            # Type distribution
            type_distribution = {}
            for ext in self.extensions.values():
                ext_type = ext.type.value
                type_distribution[ext_type] = type_distribution.get(ext_type, 0) + 1
            
            # Rating distribution
            rating_distribution = {}
            for ext in self.extensions.values():
                rating = ext.rating.value
                rating_distribution[rating] = rating_distribution.get(rating, 0) + 1
            
            return {
                "total_extensions": total_extensions,
                "total_reviews": total_reviews,
                "total_downloads": total_downloads,
                "average_rating": sum(ext.average_rating for ext in self.extensions.values()) / total_extensions if total_extensions > 0 else 0,
                "verified_extensions": len([ext for ext in self.extensions.values() if ext.is_verified]),
                "featured_extensions": len([ext for ext in self.extensions.values() if ext.is_featured]),
                "category_distribution": category_distribution,
                "type_distribution": type_distribution,
                "rating_distribution": rating_distribution,
                "marketplaces": len(self.marketplaces)
            }
            
        except Exception as e:
            logger.error(f"Failed to get marketplace statistics: {e}")
            return {}
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """Compare two version strings"""
        try:
            from packaging import version as pkg_version
            v1 = pkg_version.parse(version1)
            v2 = pkg_version.parse(version2)
            
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
            else:
                return 0
                
        except Exception:
            # Fallback to string comparison
            return 1 if version1 > version2 else (-1 if version1 < version2 else 0)


# Global instance
marketplace_service = MarketplaceService()
