import { Clock } from 'lucide-react';

function QueryHistory({ history }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-4 max-h-96 overflow-y-auto">
      <div className="flex items-center mb-4">
        <Clock className="w-5 h-5 text-indigo-600 mr-2" />
        <h3 className="font-semibold text-gray-800">Query History</h3>
      </div>

      {history.length === 0 ? (
        <p className="text-gray-500 text-sm text-center py-4">
          No queries yet
        </p>
      ) : (
        <div className="space-y-3">
          {history.slice().reverse().map((item, idx) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors">
              <p className="text-sm text-gray-800 font-medium mb-1 line-clamp-2">
                {item.question}
              </p>
              <code className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded block overflow-x-auto">
                {item.sql}
              </code>
              <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
                <span>{item.rowCount} rows</span>
                <span>{new Date(item.timestamp).toLocaleTimeString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default QueryHistory;
