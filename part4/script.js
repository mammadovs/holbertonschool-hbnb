document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesList = document.getElementById('places-list');
    const placeDetails = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews-container');
    const reviewForm = document.getElementById('review-form');

    const API_URL = 'http://127.0.0.1:5000/api/v1';

    // Global check for authentication (handles header links: Login/Logout)
    checkAuthentication();

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
        fetchPlaces();

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
    if (placeDetails) {
        const placeId = getPlaceIdFromURL();

        if (placeId) {
            const token = getCookie('token');
            const addReviewSection = document.getElementById('add-review-section');
            const reviewLink = document.getElementById('review-link');

            // Show/hide add review button based on authentication
            if (token && addReviewSection) {
                addReviewSection.style.display = 'block';
                if (reviewLink) {
                    reviewLink.href = `add_review.html?place_id=${placeId}`;
                }
            } else if (addReviewSection) {
                addReviewSection.style.display = 'none';
            }

            // Fetch place details and reviews
            fetchPlaceDetails(token, placeId);
            fetchPlaceReviews(placeId);
        } else {
            placeDetails.innerHTML = '<p>Place ID not found in URL.</p>';
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

// Check user authentication and toggle login/logout link visibility in header
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) {
            logoutLink.style.display = 'block';
            logoutLink.addEventListener('click', (e) => {
                e.preventDefault();
                document.cookie = 'token=; path=/; max-age=0';
                window.location.reload();
            });
        }
    }
}

// Get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Extract place ID from URL query parameters
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Fetch places data for index.html
async function fetchPlaces() {
    const API_URL = 'http://127.0.0.1:5000/api/v1';
    const token = getCookie('token');
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

// Populate places list dynamically on index.html
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

// Fetch place details from API for place.html
async function fetchPlaceDetails(token, placeId) {
    const API_URL = 'http://127.0.0.1:5000/api/v1';
    const headers = { 'Accept': 'application/json' };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            const placeDetails = document.getElementById('place-details');
            if (placeDetails) {
                placeDetails.innerHTML = '<p>Place details could not be loaded.</p>';
            }
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// Populate place details dynamically on place.html
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    placeDetails.innerHTML = '';

    // Format amenities if available
    let amenitiesHtml = '<p><strong>Amenities:</strong> None</p>';
    if (place.amenities && place.amenities.length > 0) {
        const amenitiesList = place.amenities.map(a => `<li>${a.name || a}</li>`).join('');
        amenitiesHtml = `<p><strong>Amenities:</strong></p><ul>${amenitiesList}</ul>`;
    }

    placeDetails.innerHTML = `
        <h2>${place.title}</h2>
        <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
        <p><strong>Price per night:</strong> $${place.price}</p>
        <p><strong>Location:</strong> Latitude: ${place.latitude}, Longitude: ${place.longitude}</p>
        ${amenitiesHtml}
    `;
}

// Fetch reviews for the place on place.html
async function fetchPlaceReviews(placeId) {
    const API_URL = 'http://127.0.0.1:5000/api/v1';
    const reviewsContainer = document.getElementById('reviews-container');
    if (!reviewsContainer) return;

    try {
        const response = await fetch(`${API_URL}/reviews/`);
        if (response.ok) {
            const reviews = await response.json();
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
    } catch (err) {
        console.error('Error fetching reviews:', err);
    }
}

