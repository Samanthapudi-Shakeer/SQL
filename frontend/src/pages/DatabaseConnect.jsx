import { useState } from 'react';
import { Database, Upload, Loader } from 'lucide-react';
import { connectSQLite, connectMySQL } from '../services/api';

function DatabaseConnect({ onConnectionSuccess }) {
  const [activeTab, setActiveTab] = useState('sqlite');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // SQLite state
  const [selectedFile, setSelectedFile] = useState(null);
  
  // MySQL state
  const [mysqlForm, setMysqlForm] = useState({
    host: 'localhost',
    port: 3306,
    database: '',
    username: '',
    password: '',
  });

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.endsWith('.db')) {
        setError('Please select a valid .db file');
        return;
      }
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleSQLiteConnect = async () => {
    if (!selectedFile) {
      setError('Please select a database file');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await connectSQLite(selectedFile);
      onConnectionSuccess(response.session_id, response.schema, 'sqlite');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to database');
    } finally {
      setLoading(false);
    }
  };

  const handleMySQLConnect = async () => {
    if (!mysqlForm.database || !mysqlForm.username) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await connectMySQL(mysqlForm);
      onConnectionSuccess(response.session_id, response.schema, 'mysql');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to MySQL');
    } finally {
      setLoading(false);
    }
  };

  const handleMysqlChange = (e) => {
    const { name, value } = e.target;
    setMysqlForm(prev => ({
      ...prev,
      [name]: name === 'port' ? parseInt(value) : value
    }));
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex items-center justify-center mb-6">
          <Database className="w-12 h-12 text-indigo-600 mr-3" />
          <h2 className="text-2xl font-bold text-gray-800">
            Connect to Database
          </h2>
        </div>

        {/* Tabs */}
        <div className="flex mb-6 border-b">
          <button
            className={`flex-1 py-3 px-4 font-medium ${
              activeTab === 'sqlite'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
            onClick={() => {
              setActiveTab('sqlite');
              setError(null);
            }}
          >
            SQLite Upload
          </button>
          <button
            className={`flex-1 py-3 px-4 font-medium ${
              activeTab === 'mysql'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
            onClick={() => {
              setActiveTab('mysql');
              setError(null);
            }}
          >
            MySQL Connection
          </button>
        </div>

        {/* SQLite Tab */}
        {activeTab === 'sqlite' && (
          <div>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition-colors">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">
                Upload your SQLite database file (.db)
              </p>
              <input
                type="file"
                accept=".db"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-block bg-indigo-600 text-white px-6 py-2 rounded-lg cursor-pointer hover:bg-indigo-700 transition-colors"
              >
                Choose File
              </label>
              {selectedFile && (
                <p className="mt-4 text-sm text-gray-600">
                  Selected: <span className="font-medium">{selectedFile.name}</span>
                </p>
              )}
            </div>
            <button
              onClick={handleSQLiteConnect}
              disabled={loading || !selectedFile}
              className="w-full mt-6 bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 mr-2 animate-spin" />
                  Connecting...
                </>
              ) : (
                'Connect to Database'
              )}
            </button>
          </div>
        )}

        {/* MySQL Tab */}
        {activeTab === 'mysql' && (
          <div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Host
                </label>
                <input
                  type="text"
                  name="host"
                  value={mysqlForm.host}
                  onChange={handleMysqlChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  placeholder="localhost"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Port
                </label>
                <input
                  type="number"
                  name="port"
                  value={mysqlForm.port}
                  onChange={handleMysqlChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  placeholder="3306"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Database Name *
                </label>
                <input
                  type="text"
                  name="database"
                  value={mysqlForm.database}
                  onChange={handleMysqlChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  placeholder="my_database"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Username *
                </label>
                <input
                  type="text"
                  name="username"
                  value={mysqlForm.username}
                  onChange={handleMysqlChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  placeholder="root"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  value={mysqlForm.password}
                  onChange={handleMysqlChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  placeholder="••••••••"
                />
              </div>
            </div>
            <button
              onClick={handleMySQLConnect}
              disabled={loading}
              className="w-full mt-6 bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 mr-2 animate-spin" />
                  Connecting...
                </>
              ) : (
                'Connect to MySQL'
              )}
            </button>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default DatabaseConnect;
