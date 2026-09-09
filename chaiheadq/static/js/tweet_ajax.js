// Minimal AJAX helper for posting tweets
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function handleTweetForm(event) {
  const form = event.target;
  if (!form || form.dataset.noAjax === "true") return;
  event.preventDefault();
  const url = form.action || window.location.href;
  const formData = new FormData(form);
  const resp = await fetch(url, {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken') || ''
    },
  });
  if (resp.ok) {
    try {
      const data = await resp.json();
      // simple client-side insertion: prepend to tweet list if present
      const container = document.querySelector('.row.g-3');
      if (container && data.html) {
        const wrapper = document.createElement('div');
        wrapper.className = 'col-12 col-md-6 col-lg-4';
        wrapper.innerHTML = data.html;
        container.prepend(wrapper);
        form.reset();
      } else if (data.redirect) {
        window.location = data.redirect;
      }
    } catch (err) {
      // fallback: reload
      window.location.reload();
    }
  } else {
    // on failure, fallback to normal behavior
    window.location.reload();
  }
}

document.addEventListener('submit', function (e) {
  if (e.target && e.target.matches && e.target.matches('#tweet-form')) {
    handleTweetForm(e);
  }
});
