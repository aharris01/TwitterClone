let offset = 10;
const loadMoreBtn = document.getElementById('loadMoreBtn');
const postsContainer = document.getElementById('posts-container')

loadMoreBtn.addEventListener('click', async () => {
    try {
        const url = `/api/recentposts?offset=${offset}`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error loading posts: ${response.statusText}`);
        }

        const newPosts = await response.json();

        if (newPosts.length === 0) {
            loadMoreBtn.innerText = "No more posts";
            loadMoreBtn.disabled = true;
            return
        }

        newPosts.forEach(post => {
            const postDiv = document.createElement('div');
            postDiv.classList.add('post');
            postDiv.innerHTML = `
                  <p>${post.content}</p>
                  <small>Posted on ${post.createdAt}</small>
                `;
            postsContainer.appendChild(postDiv);
        });

        offset += newPosts.length;
    } catch (error) {
        console.error(error);
        alert("Failed to load more posts.");
    }
});