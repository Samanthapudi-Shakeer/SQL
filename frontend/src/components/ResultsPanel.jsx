import { useState } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Table as TableIcon, BarChart3, LineChart as LineChartIcon, PieChart as PieChartIcon } from 'lucide-react';

const COLORS = ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

function ResultsPanel({ results, sql, chartConfig }) {
  const [activeView, setActiveView] = useState('table');

  const renderChart = () => {
    if (!chartConfig || !results?.data) return null;

    const data = results.data;

    if (chartConfig.chart_type === 'bar' && chartConfig.x_axis && chartConfig.y_axis) {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={chartConfig.x_axis} />
            <YAxis />
            <Tooltip />
            <Legend />
            {chartConfig.y_axis.map((yKey, idx) => (
              <Bar key={yKey} dataKey={yKey} fill={COLORS[idx % COLORS.length]} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      );
    }

    if (chartConfig.chart_type === 'line' && chartConfig.x_axis && chartConfig.y_axis) {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={chartConfig.x_axis} />
            <YAxis />
            <Tooltip />
            <Legend />
            {chartConfig.y_axis.map((yKey, idx) => (
              <Line key={yKey} type="monotone" dataKey={yKey} stroke={COLORS[idx % COLORS.length]} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      );
    }

    if (chartConfig.chart_type === 'pie' && chartConfig.labels && chartConfig.values) {
      const pieData = chartConfig.labels.map((label, idx) => ({
        name: label,
        value: chartConfig.values[idx]
      }));

      return (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {pieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      );
    }

    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="p-4 border-b">
        <h3 className="font-semibold text-gray-800 mb-2">Results</h3>
        
        {/* View Toggle */}
        <div className="flex gap-2 mt-3">
          <button
            onClick={() => setActiveView('table')}
            className={`flex items-center px-3 py-1.5 rounded-lg text-sm ${
              activeView === 'table'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <TableIcon className="w-4 h-4 mr-1" />
            Table
          </button>
          {chartConfig && chartConfig.chart_type !== 'table' && (
            <button
              onClick={() => setActiveView('chart')}
              className={`flex items-center px-3 py-1.5 rounded-lg text-sm ${
                activeView === 'chart'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {chartConfig.chart_type === 'bar' && <BarChart3 className="w-4 h-4 mr-1" />}
              {chartConfig.chart_type === 'line' && <LineChartIcon className="w-4 h-4 mr-1" />}
              {chartConfig.chart_type === 'pie' && <PieChartIcon className="w-4 h-4 mr-1" />}
              Chart
            </button>
          )}
        </div>
      </div>

      <div className="p-4 max-h-96 overflow-auto">
        {activeView === 'table' && (
          <>
            {/* SQL Display */}
            {sql && (
              <div className="mb-4 p-3 bg-gray-800 text-green-400 rounded text-xs font-mono overflow-x-auto">
                {sql}
              </div>
            )}

            {/* Table */}
            {results?.data && results.data.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      {results.columns.map((col) => (
                        <th
                          key={col}
                          className="px-4 py-2 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
                        >
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {results.data.map((row, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        {results.columns.map((col) => (
                          <td key={col} className="px-4 py-2 whitespace-nowrap text-gray-900">
                            {row[col] !== null ? String(row[col]) : <span className="text-gray-400">NULL</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No results to display</p>
            )}

            <p className="text-sm text-gray-600 mt-4">
              {results?.row_count || 0} rows returned
            </p>
          </>
        )}

        {activeView === 'chart' && (
          <div className="py-4">
            {chartConfig && chartConfig.title && (
              <h4 className="text-center font-medium text-gray-800 mb-4">
                {chartConfig.title}
              </h4>
            )}
            {renderChart()}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsPanel;
