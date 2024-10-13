// import { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { useToast } from '../utils/ToastMessage';

// export const useFetchMovies = (searchQuery, currentPageUrl, setLoading, setMovies) => {
//     const [totalPages, setTotalPages] = useState(1);
//     const navigate = useNavigate();
//     const { showToast } = useToast();

//     useEffect(() => {

//         const fetchMovies = async () => {
//             setLoading(true); // Trigger loading before the fetch
//             try {
//                 const token = localStorage.getItem('token');
//                 if (!token) {
//                     navigate("/login");
//                     return;
//                 }

//                 const url = searchQuery
//                     ? `http://localhost:5000/wishlist/search?query=${searchQuery}&page=${currentPageUrl}`
//                     : `http://localhost:5000/wishlist?page=${currentPageUrl}`;

//                 const response = await fetch(url, {
//                     method: 'GET',
//                     headers: {
//                         'Authorization': `Bearer ${token}`,
//                         'Content-Type': 'application/json',
//                     },
//                     credentials: 'include',
//                     mode: 'cors',
//                 });

//                 if (response.status === 401) {
//                     navigate('/login');
//                 }

//                 const result = await response.json();
//                 if (response.ok) {
//                     setMovies(result.results);
//                     setTotalPages(result.total_pages || 1);
//                 } else {
//                     showToast(result.error);
//                 }
//             } catch (error) {
//                 console.error('Error fetching movies:', error);
//             } finally {
//                 setLoading(false);  // Turn off loading after the fetch is done
//             }
//         };

//         fetchMovies();
//     }, [searchQuery, currentPageUrl, navigate, showToast]);

//     return { totalPages };

// };