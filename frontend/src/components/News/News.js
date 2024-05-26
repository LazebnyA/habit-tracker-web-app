import React, {useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
import './News.css'
import axios from "axios";

const News = () => {
    const [newsItems, setNewsItems] = useState(null)

    const getNews = async () => {
        const response = await axios.get(`http://127.0.0.1:8000/news/get`, {
          headers: {
              'accept': 'application/json'
          }
        })
        return response.data
    }

    useEffect(() => {
        const fetchNews = async () => {
            const news = await getNews();
            setNewsItems(news);
        };

        fetchNews();
    }, []);

    return (
        <>
            <nav id="newsNav">
                <div className="navContainer">
                    <h1><Link to="/">Evolve</Link></h1>
                    <ul>
                        <li><Link className="navButton" to="/">Home</Link></li>
                        <li><Link className="navButton" to="/Signin">Login</Link></li>
                        <li><Link className="navButton" to="/Register">Register</Link></li>
                    </ul>
                </div>
            </nav>

            <header id="newsHeader">
                <div className="newsContainer">
                    <div className="newsHeading">
                        <h1>What's New</h1>
                        <p>Stay updated with the latest news and release notes from Evolve.</p>
                    </div>
                </div>
            </header>

            <main>
                <section className="news">
                    <div className="newsContainer">
                        {newsItems && newsItems.map((item, index) => (
                            <div className="newsItem" key={index}>
                                <h2>{item.title}</h2>
                                <p className="date">{item.created_date}</p>
                                <p>{item.content}</p>
                            </div>
                        ))}
                    </div>
                </section>
            </main>

            <footer>
                <div className="container">
                    <p>&copy; 2024 Evolve</p>
                </div>
            </footer>
        </>
    );
};

export default News;