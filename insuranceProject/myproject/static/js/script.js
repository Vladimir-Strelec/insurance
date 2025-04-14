fetch('/your-url/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCSRFToken()
  },
  body: JSON.stringify(data)
});

function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

