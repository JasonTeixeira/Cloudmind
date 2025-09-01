/**
 * Advanced Data Table Component
 * Features: Sorting, filtering, pagination, selection, export
 */

import React, { useState, useMemo, useCallback } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  ChevronDownIcon, 
  ChevronUpIcon,
  FilterIcon,
  DownloadIcon,
  MoreHorizontalIcon,
  SearchIcon,
  RefreshCwIcon
} from 'lucide-react';

export interface Column<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  filterable?: boolean;
  width?: string;
  render?: (value: any, row: T) => React.ReactNode;
  align?: 'left' | 'center' | 'right';
}

export interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  loading?: boolean;
  selectable?: boolean;
  onSelectionChange?: (selectedRows: T[]) => void;
  onRowClick?: (row: T) => void;
  onExport?: (data: T[], format: 'csv' | 'excel' | 'pdf') => void;
  pagination?: {
    pageSize: number;
    currentPage: number;
    total: number;
    onPageChange: (page: number) => void;
  };
  searchable?: boolean;
  filterable?: boolean;
  sortable?: boolean;
  className?: string;
  emptyMessage?: string;
  rowActions?: (row: T) => Array<{
    label: string;
    onClick: () => void;
    icon?: React.ReactNode;
    variant?: 'default' | 'destructive';
  }>;
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  loading = false,
  selectable = false,
  onSelectionChange,
  onRowClick,
  onExport,
  pagination,
  searchable = true,
  filterable = true,
  sortable = true,
  className = '',
  emptyMessage = 'No data available',
  rowActions,
}: DataTableProps<T>) {
  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());
  const [sortConfig, setSortConfig] = useState<{
    key: keyof T;
    direction: 'asc' | 'desc';
  } | null>(null);
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [searchTerm, setSearchTerm] = useState('');

  // Generate unique row IDs
  const getRowId = useCallback((row: T, index: number) => {
    return row.id || row.key || `row-${index}`;
  }, []);

  // Filter data based on search and filters
  const filteredData = useMemo(() => {
    let filtered = data;

    // Apply search
    if (searchTerm) {
      filtered = filtered.filter(row =>
        Object.values(row).some(value =>
          String(value).toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }

    // Apply filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value) {
        filtered = filtered.filter(row => {
          const cellValue = row[key];
          return String(cellValue).toLowerCase().includes(value.toLowerCase());
        });
      }
    });

    return filtered;
  }, [data, searchTerm, filters]);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortConfig) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (aValue < bValue) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }, [filteredData, sortConfig]);

  // Handle sorting
  const handleSort = useCallback((key: keyof T) => {
    setSortConfig(current => {
      if (current?.key === key) {
        return {
          key,
          direction: current.direction === 'asc' ? 'desc' : 'asc',
        };
      }
      return { key, direction: 'asc' };
    });
  }, []);

  // Handle selection
  const handleSelectRow = useCallback((rowId: string, checked: boolean) => {
    const newSelected = new Set(selectedRows);
    if (checked) {
      newSelected.add(rowId);
    } else {
      newSelected.delete(rowId);
    }
    setSelectedRows(newSelected);

    if (onSelectionChange) {
      const selectedData = data.filter(row => newSelected.has(getRowId(row, 0)));
      onSelectionChange(selectedData);
    }
  }, [selectedRows, data, onSelectionChange, getRowId]);

  // Handle select all
  const handleSelectAll = useCallback((checked: boolean) => {
    if (checked) {
      const allIds = new Set(sortedData.map((row, index) => getRowId(row, index)));
      setSelectedRows(allIds);
      if (onSelectionChange) {
        onSelectionChange(sortedData);
      }
    } else {
      setSelectedRows(new Set());
      if (onSelectionChange) {
        onSelectionChange([]);
      }
    }
  }, [sortedData, onSelectionChange, getRowId]);

  // Handle export
  const handleExport = useCallback((format: 'csv' | 'excel' | 'pdf') => {
    if (onExport) {
      const exportData = selectedRows.size > 0 
        ? data.filter(row => selectedRows.has(getRowId(row, 0)))
        : sortedData;
      onExport(exportData, format);
    }
  }, [onExport, selectedRows, data, sortedData, getRowId]);

  // Render cell content
  const renderCell = useCallback((column: Column<T>, row: T, rowIndex: number) => {
    const value = row[column.key];
    
    if (column.render) {
      return column.render(value, row);
    }

    // Default rendering based on data type
    if (typeof value === 'boolean') {
      return (
        <Badge variant={value ? 'default' : 'secondary'}>
          {value ? 'Yes' : 'No'}
        </Badge>
      );
    }

    if (typeof value === 'number') {
      return value.toLocaleString();
    }

    if (value instanceof Date) {
      return value.toLocaleDateString();
    }

    return String(value || '');
  }, []);

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">
            Data Table ({sortedData.length} items)
          </CardTitle>
          
          <div className="flex items-center gap-2">
            {onExport && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm">
                    <DownloadIcon className="h-4 w-4 mr-2" />
                    Export
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuLabel>Export Format</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => handleExport('csv')}>
                    Export as CSV
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleExport('excel')}>
                    Export as Excel
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleExport('pdf')}>
                    Export as PDF
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
          </div>
        </div>

        {/* Search and Filters */}
        <div className="flex items-center gap-4">
          {searchable && (
            <div className="relative flex-1 max-w-sm">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          )}

          {filterable && (
            <div className="flex items-center gap-2">
              {columns
                .filter(col => col.filterable)
                .map(column => (
                  <div key={String(column.key)} className="flex items-center gap-1">
                    <FilterIcon className="h-4 w-4 text-gray-400" />
                    <Input
                      placeholder={`Filter ${column.header}`}
                      value={filters[String(column.key)] || ''}
                      onChange={(e) => setFilters(prev => ({
                        ...prev,
                        [String(column.key)]: e.target.value
                      }))}
                      className="w-32"
                    />
                  </div>
                ))}
            </div>
          )}

          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setSearchTerm('');
              setFilters({});
              setSortConfig(null);
            }}
          >
            <RefreshCwIcon className="h-4 w-4 mr-2" />
            Clear
          </Button>
        </div>
      </CardHeader>

      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <RefreshCwIcon className="h-6 w-6 animate-spin mr-2" />
            Loading...
          </div>
        ) : sortedData.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            {emptyMessage}
          </div>
        ) : (
          <>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    {selectable && (
                      <TableHead className="w-12">
                        <Checkbox
                          checked={selectedRows.size === sortedData.length && sortedData.length > 0}
                          onCheckedChange={handleSelectAll}
                        />
                      </TableHead>
                    )}
                    {columns.map(column => (
                      <TableHead
                        key={String(column.key)}
                        className={column.width ? `w-[${column.width}]` : ''}
                        style={{ textAlign: column.align || 'left' }}
                      >
                        <div className="flex items-center gap-2">
                          <span>{column.header}</span>
                          {sortable && column.sortable && (
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleSort(column.key)}
                              className="h-6 w-6 p-0"
                            >
                              {sortConfig?.key === column.key ? (
                                sortConfig.direction === 'asc' ? (
                                  <ChevronUpIcon className="h-4 w-4" />
                                ) : (
                                  <ChevronDownIcon className="h-4 w-4" />
                                )
                              ) : (
                                <ChevronDownIcon className="h-4 w-4 opacity-50" />
                              )}
                            </Button>
                          )}
                        </div>
                      </TableHead>
                    ))}
                    {rowActions && <TableHead className="w-12">Actions</TableHead>}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedData.map((row, rowIndex) => (
                    <TableRow
                      key={getRowId(row, rowIndex)}
                      className={onRowClick ? 'cursor-pointer hover:bg-gray-50' : ''}
                      onClick={() => onRowClick?.(row)}
                    >
                      {selectable && (
                        <TableCell>
                          <Checkbox
                            checked={selectedRows.has(getRowId(row, rowIndex))}
                            onCheckedChange={(checked) => 
                              handleSelectRow(getRowId(row, rowIndex), checked as boolean)
                            }
                            onClick={(e) => e.stopPropagation()}
                          />
                        </TableCell>
                      )}
                      {columns.map(column => (
                        <TableCell
                          key={String(column.key)}
                          style={{ textAlign: column.align || 'left' }}
                        >
                          {renderCell(column, row, rowIndex)}
                        </TableCell>
                      ))}
                      {rowActions && (
                        <TableCell>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={(e) => e.stopPropagation()}
                              >
                                <MoreHorizontalIcon className="h-4 w-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent>
                              {rowActions(row).map((action, index) => (
                                <DropdownMenuItem
                                  key={index}
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    action.onClick();
                                  }}
                                  className={action.variant === 'destructive' ? 'text-red-600' : ''}
                                >
                                  {action.icon}
                                  {action.label}
                                </DropdownMenuItem>
                              ))}
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      )}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Pagination */}
            {pagination && (
              <div className="flex items-center justify-between mt-4">
                <div className="text-sm text-gray-500">
                  Showing {((pagination.currentPage - 1) * pagination.pageSize) + 1} to{' '}
                  {Math.min(pagination.currentPage * pagination.pageSize, pagination.total)} of{' '}
                  {pagination.total} results
                </div>
                
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => pagination.onPageChange(pagination.currentPage - 1)}
                    disabled={pagination.currentPage === 1}
                  >
                    Previous
                  </Button>
                  
                  <span className="text-sm">
                    Page {pagination.currentPage} of{' '}
                    {Math.ceil(pagination.total / pagination.pageSize)}
                  </span>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => pagination.onPageChange(pagination.currentPage + 1)}
                    disabled={
                      pagination.currentPage >= Math.ceil(pagination.total / pagination.pageSize)
                    }
                  >
                    Next
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
} 