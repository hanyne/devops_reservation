export default function Login() {
    const handleLogin = () => {
      window.location.href = 'http://localhost:5000/auth/login';
    };
  
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-6 rounded shadow-md">
          <h2 className="text-2xl font-bold mb-4">Connexion</h2>
          <button
            onClick={handleLogin}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Se connecter avec Google
          </button>
        </div>
      </div>
    );
  }