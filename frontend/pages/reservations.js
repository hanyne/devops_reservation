import { useEffect, useState } from 'react';

export default function Reservations() {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    fetch('http://localhost:5000/reservations', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setReservations(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleCancel = (id) => {
    const token = localStorage.getItem('token');
    fetch(`http://localhost:5000/reservations/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(() => {
        setReservations(reservations.filter((res) => res.id !== id));
      })
      .catch((err) => console.error(err));
  };

  if (loading) return <p>Chargement...</p>;

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-4">Mes Réservations</h1>
      <ul className="space-y-4">
        {reservations.map((res) => (
          <li key={res.id} className="bg-white p-4 rounded shadow">
            <p>Salle ID: {res.salle_id}</p>
            <p>Début: {res.start_time}</p>
            <p>Fin: {res.end_time}</p>
            <p>Statut: {res.status}</p>
            {res.status === 'Confirmée' && (
              <button
                onClick={() => handleCancel(res.id)}
                className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
              >
                Annuler
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}