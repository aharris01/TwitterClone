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
                  <div class="post">
                    <div class="post-header">
                        <span class="post-author">${post.author}</span>
                        <span class="post-time">${post.createdAt}</span>
                    </div>
                    <p>${post.content}</p>
                    <!--jinja2 automatically encodes special characters like <, >, etc. so if backend validation fails this should catch anything else-->
                </div>
                `;
            postsContainer.appendChild(postDiv);
        });

        offset += newPosts.length;
    } catch (error) {
        console.error(error);
        alert("Failed to load more posts.");
    }
});