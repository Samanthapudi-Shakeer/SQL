import { useState } from 'react';
import { ChevronDown, ChevronRight, Table, Key } from 'lucide-react';

function SchemaPanel({ schema, dbType }) {
  const [expandedTables, setExpandedTables] = useState({});

  const toggleTable = (tableName) => {
    setExpandedTables(prev => ({
      ...prev,
      [tableName]: !prev[tableName]
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 h-[calc(100vh-12rem)] overflow-y-auto">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-gray-800 mb-1">
          Database Schema
        </h2>
        <p className="text-sm text-gray-600">
          {dbType?.toUpperCase()} • {schema?.tables?.length || 0} tables
        </p>
      </div>

      <div className="space-y-2">
        {schema?.tables?.map((table) => (
          <div key={table.name} className="border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleTable(table.name)}
              className="w-full flex items-center justify-between p-3 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center">
                <Table className="w-4 h-4 text-indigo-600 mr-2" />
                <span className="font-medium text-gray-800">{table.name}</span>
              </div>
              {expandedTables[table.name] ? (
                <ChevronDown className="w-4 h-4 text-gray-600" />
              ) : (
                <ChevronRight className="w-4 h-4 text-gray-600" />
              )}
            </button>

            {expandedTables[table.name] && (
              <div className="bg-gray-50 p-3 border-t">
                <div className="space-y-2">
                  {table.columns.map((column) => (
                    <div key={column.name} className="flex items-start text-sm">
                      <div className="flex-1">
                        <div className="flex items-center">
                          {column.primary_key && (
                            <Key className="w-3 h-3 text-yellow-600 mr-1" />
                          )}
                          <span className="font-medium text-gray-800">
                            {column.name}
                          </span>
                        </div>
                        <div className="text-gray-600 text-xs mt-0.5">
                          {column.type}
                          {column.primary_key && ' • PK'}
                          {column.foreign_key && ` • FK → ${column.foreign_key}`}
                          {!column.nullable && ' • NOT NULL'}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SchemaPanel;
