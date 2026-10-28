document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesList = document.getElementById('places-list');
    const placeDetailsContainer = document.getElementById('place-details-container');
    const reviewsContainer = document.getElementById('reviews-container');
    const reviewForm = document.getElementById('review-form');

    const API_URL = 'http://127.0.0.1:5000/api/v1';

    // ==========================================
    // 1. Login Logic (login.html)
    // ==========================================
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Store token in cookies
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
                    window.location.href = 'index.html';
                } else {
                    const errData = await response.json();
                    alert(errData.error || 'Login failed');
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('Connection error');
            }
        });
    }

    // ==========================================
    // 2. Index Page Logic (index.html)
    // ==========================================
    if (placesList) {
        // Check user authentication on page load
        checkAuthentication();

        // Price filter event listener
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                const selectedPrice = event.target.value;
                const placeCards = document.querySelectorAll('.place-card');

                placeCards.forEach(card => {
                    const price = parseFloat(card.getAttribute('data-price'));
                    if (selectedPrice === 'All' || price <= parseFloat(selectedPrice)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        }
    }

    // ==========================================
    // 3. Place Details Logic (place.html)
    // ==========================================
    if (placeDetailsContainer) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');

        if (placeId) {
            // Fetch place details
            fetch(`${API_URL}/places/${placeId}`)
                .then(res => {
                    if (!res.ok) throw new Error('Place not found');
                    return res.json();
                })
                .then(place => {
                    placeDetailsContainer.innerHTML = `
                        <h2>${place.title}</h2>
                        <p><strong>Description:</strong> ${place.description}</p>
                        <p><strong>Price per night:</strong> $${place.price}</p>
                        <p><strong>Location:</strong> Lat: ${place.latitude}, Lon: ${place.longitude}</p>
                    `;
                    
                    // Show add review button/form if authenticated
                    const token = getCookie('token');
                    const addReviewSection = document.getElementById('add-review-section');
                    if (token && addReviewSection) {
                        addReviewSection.style.display = 'block';
                    }
                })
                .catch(err => {
                    console.error(err);
                    placeDetailsContainer.innerHTML = '<p>Place details could not be loaded.</p>';
                });

            // Fetch reviews for this place
            fetch(`${API_URL}/reviews/`)
                .then(res => res.json())
                .then(reviews => {
                    if (reviewsContainer) {
                        reviewsContainer.innerHTML = '';
                        const placeReviews = reviews.filter(r => r.place_id === placeId);
                        if (placeReviews.length === 0) {
                            reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
                            return;
                        }
                        placeReviews.forEach(review => {
                            const reviewCard = document.createElement('div');
                            reviewCard.className = 'review-card';
                            reviewCard.innerHTML = `
                                <p><strong>Rating:</strong> ${review.rating} / 5</p>
                                <p>${review.text}</p>
                            `;
                            reviewsContainer.appendChild(reviewCard);
                        });
                    }
                })
                .catch(err => console.error('Error fetching reviews:', err));
        }
    }

    // ==========================================
    // 4. Add Review Logic (add_review.html)
    // ==========================================
    if (reviewForm) {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }

        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id');

        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const rating = parseInt(document.getElementById('rating').value);
            const text = document.getElementById('text').value;

            try {
                const response = await fetch(`${API_URL}/reviews/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ place_id: placeId, rating, text })
                });

                if (response.ok) {
                    window.location.href = `place.html?id=${placeId}`;
                } else {
                    const errData = await response.json();
                    alert(errData.error || 'Failed to submit review');
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('Connection error');
            }
        });
    }
});

// ==========================================
// Helper Functions
// ==========================================

// Check user authentication and toggle login/logout link visibility
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
        fetchPlaces(); // Fetch places without token
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) {
            logoutLink.style.display = 'block';
            // Add click event to logout
            logoutLink.addEventListener('click', (e) => {
                e.preventDefault();
                // Delete cookie by setting max-age to 0
                document.cookie = 'token=; path=/; max-age=0';
                window.location.reload();
            });
        }
        fetchPlaces(token); // Fetch places with token
    }
}

// Get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Fetch places data from API
async function fetchPlaces(token = '') {
    const API_URL = 'http://127.0.0.1:5000/api/v1';
    const headers = { 'Accept': 'application/json' };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_URL}/places/`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// Populate places list dynamically
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        // Store price as an attribute for client-side filtering
        card.setAttribute('data-price', place.price);

        card.innerHTML = `
            <h3>${place.title}</h3>
            <p>Price: $${place.price} / night</p>
            <p>${place.description || ''}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}

