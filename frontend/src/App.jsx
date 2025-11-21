import { useState } from 'react';
import DatabaseConnect from './pages/DatabaseConnect';
import QueryInterface from './pages/QueryInterface';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [schema, setSchema] = useState(null);
  const [dbType, setDbType] = useState(null);

  const handleConnectionSuccess = (session, schemaData, type) => {
    setSessionId(session);
    setSchema(schemaData);
    setDbType(type);
  };

  const handleDisconnect = () => {
    setSessionId(null);
    setSchema(null);
    setDbType(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-indigo-600">
            AskQL
          </h1>
          <p className="text-gray-600 mt-1">
            Convert Natural Language to SQL Queries
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {!sessionId ? (
          <DatabaseConnect onConnectionSuccess={handleConnectionSuccess} />
        ) : (
          <QueryInterface
            sessionId={sessionId}
            schema={schema}
            dbType={dbType}
            onDisconnect={handleDisconnect}
          />
        )}
      </main>

      <footer className="text-center py-8 text-gray-600">
        <p>AskQL v1.0.0 - Natural Language to SQL Converter</p>
      </footer>
    </div>
  );
}

export default App;
