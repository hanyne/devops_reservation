import { useEffect, useState } from 'react';

export default function Salles() {
  const [salles, setSalles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    fetch('http://localhost:5000/salles', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setSalles(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Chargement...</p>;

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-4">Liste des Salles</h1>
      <ul className="space-y-4">
        {salles.map((salle) => (
          <li key={salle.id} className="bg-white p-4 rounded shadow">
            <h2 className="text-xl">{salle.name}</h2>
            <p>Capacité: {salle.capacity}</p>
            <p>Disponible: {salle.available ? 'Oui' : 'Non'}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}