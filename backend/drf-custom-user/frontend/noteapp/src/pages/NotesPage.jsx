import React, { useState } from 'react';
import axios from 'axios';

function NotesPage() {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const user = localStorage.getItem('userEmail'); // Get user's email from localstorage
    const accessToken = localStorage.getItem('accessToken'); // Get access token from localStorage

    const handleCreateNote = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/notes/',
                { user, title, content },
                {
                    headers: {
                        Authorization: `Bearer ${accessToken}`, // Include access token in the request header
                    },
                }
            );
            console.log('Note created:', response.data);
        } catch (error) {
            console.error('Failed to create note:', error.response || error.message);
            alert('Failed to create note!');
        }
    };

    return (
        <form onSubmit={handleCreateNote}>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Note Title"
                required
            />
            <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Note Content"
                required
            />
            <button type="submit">Create Note</button>
        </form>
    );
}

export default NotesPage;
