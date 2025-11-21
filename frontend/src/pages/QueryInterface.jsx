import { useState } from 'react';
import { Send, LogOut, Loader, Database } from 'lucide-react';
import { askQuestion, executeQuery, visualizeData } from '../services/api';
import SchemaPanel from '../components/SchemaPanel';
import ResultsPanel from '../components/ResultsPanel';
import QueryHistory from '../components/QueryHistory';

function QueryInterface({ sessionId, schema, dbType, onDisconnect }) {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [currentSQL, setCurrentSQL] = useState(null);
  const [results, setResults] = useState(null);
  const [chartConfig, setChartConfig] = useState(null);
  const [history, setHistory] = useState([]);

  const handleSendQuestion = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question;
    setQuestion('');
    setLoading(true);

    // Add user message to conversation
    const newMessage = { role: 'user', content: userQuestion };
    setConversation(prev => [...prev, newMessage]);

    try {
      // Ask question (generate SQL)
      const context = conversation.slice(-4); // Last 2 exchanges
      const sqlResponse = await askQuestion({
        question: userQuestion,
        session_id: sessionId,
        context: context.map(msg => ({
          question: msg.role === 'user' ? msg.content : '',
          answer: msg.role === 'assistant' ? msg.content : ''
        }))
      });

      if (sqlResponse.needs_clarification) {
        // Add clarification request to conversation
        setConversation(prev => [...prev, {
          role: 'assistant',
          content: sqlResponse.clarification_question,
          type: 'clarification'
        }]);
        setLoading(false);
        return;
      }

      // Store SQL
      setCurrentSQL(sqlResponse.sql);

      // Execute SQL automatically
      const execResponse = await executeQuery({
        sql: sqlResponse.sql,
        session_id: sessionId
      });

      setResults(execResponse);

      // Generate visualization
      if (execResponse.data.length > 0) {
        const vizResponse = await visualizeData({
          data: execResponse.data,
          columns: execResponse.columns
        });
        setChartConfig(vizResponse);
      }

      // Add assistant response
      setConversation(prev => [...prev, {
        role: 'assistant',
        content: sqlResponse.explanation,
        sql: sqlResponse.sql,
        results: execResponse,
        type: 'answer'
      }]);

      // Update history
      setHistory(prev => [...prev, {
        question: userQuestion,
        sql: sqlResponse.sql,
        rowCount: execResponse.row_count,
        timestamp: new Date().toISOString()
      }]);

    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Failed to process question';
      setConversation(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${errorMsg}`,
        type: 'error'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendQuestion();
    }
  };

  return (
    <div className="grid grid-cols-12 gap-6">
      {/* Left Sidebar - Schema */}
      <div className="col-span-3">
        <SchemaPanel schema={schema} dbType={dbType} />
      </div>

      {/* Main Content - Chat */}
      <div className="col-span-6">
        <div className="bg-white rounded-lg shadow-lg h-[calc(100vh-12rem)] flex flex-col">
          {/* Header */}
          <div className="p-4 border-b flex items-center justify-between">
            <div className="flex items-center">
              <Database className="w-5 h-5 text-indigo-600 mr-2" />
              <h2 className="font-semibold text-gray-800">Query Chat</h2>
            </div>
            <button
              onClick={onDisconnect}
              className="flex items-center text-red-600 hover:text-red-700 text-sm"
            >
              <LogOut className="w-4 h-4 mr-1" />
              Disconnect
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {conversation.length === 0 && (
              <div className="text-center text-gray-500 mt-8">
                <p className="text-lg font-medium mb-2">Ask me anything about your data!</p>
                <p className="text-sm">Try questions like:</p>
                <ul className="text-sm mt-2 space-y-1 text-left max-w-md mx-auto">
                  <li>• "Show me all records from the users table"</li>
                  <li>• "What are the total sales by category?"</li>
                  <li>• "Find the top 10 customers by revenue"</li>
                </ul>
              </div>
            )}

            {conversation.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white'
                      : msg.type === 'error'
                      ? 'bg-red-50 text-red-800 border border-red-200'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                  {msg.sql && (
                    <div className="mt-3 p-3 bg-gray-800 text-green-400 rounded font-mono text-sm overflow-x-auto">
                      {msg.sql}
                    </div>
                  )}
                  {msg.results && (
                    <div className="mt-2 text-sm opacity-75">
                      Returned {msg.results.row_count} rows
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg p-4 flex items-center">
                  <Loader className="w-5 h-5 animate-spin text-indigo-600 mr-2" />
                  <span className="text-gray-600">Processing...</span>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about your data..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                disabled={loading}
              />
              <button
                onClick={handleSendQuestion}
                disabled={loading || !question.trim()}
                className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Results & History */}
      <div className="col-span-3 space-y-6">
        {results && (
          <ResultsPanel 
            results={results} 
            sql={currentSQL}
            chartConfig={chartConfig}
          />
        )}
        <QueryHistory history={history} />
      </div>
    </div>
  );
}

export default QueryInterface;
