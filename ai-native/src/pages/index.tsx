import React from 'react';
import type { ReactNode } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const topics = [
  {
    title: 'Introduction to Physical AI',
    slug: 'intro/ch1-intro-physical-ai',
    description: 'Learn the fundamentals of Physical AI and Humanoid Robotics.',
  },
  {
    title: 'ROS2 Basics',
    slug: 'ros2-basics/ch2-ros2-basics',
    description: 'Get started with the Robot Operating System 2 (ROS2).',
  },
  {
    title: 'LLM and ROS2 Integration',
    slug: 'llm-ros2-integration/ch3-llm-ros2-integration',
    description: 'Integrate Large Language Models with ROS2.',
  },
  {
    title: 'Building ROS2 Packages',
    slug: 'building-ros2-packages/index',
    description: 'Create your own ROS2 packages from scratch.',
  },
];

const logos = [
  'https://www.apc.com/img/APC-logo-260x78.png',
  'https://www.se.com/ww/en/assets/260x78-SE_logo.png',
];

function Homepage(): ReactNode {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`Physical AI & Humanoid Robotics`}
      description="A book about Physical AI and Humanoid Robotics with ROS2 and LLMs"
    >
      <header className="hero-section">
        <div className="hero-content">
          <h1>Physical AI & Humanoid Robotics</h1>
          <p>
            An open-source book on Physical AI and Humanoid Robotics, covering everything from the basics to advanced topics like ROS2 and LLM integration.
          </p>
          <div className="hero-buttons">
            <Link className="button button--primary" to="/docs/01-intro">
              Read the book
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="as-seen-on">
          <h2>As seen on</h2>
          <div className="logos">
            {logos.map((logo, index) => (
              <img key={index} src={logo} alt={`Logo ${index + 1}`} />
            ))}
          </div>
        </section>

        <section className="topics-section">
          <h2>Book Chapters</h2>
          <div className="topics-grid">
            {topics.map((topic) => (
              <div key={topic.slug} className="topic-card">
                <h3>{topic.title}</h3>
                <p>{topic.description}</p>
                <Link to={`/docs/${topic.slug}`}>Read more</Link>
              </div>
            ))}
          </div>
        </section>
      </main>
    </Layout>
  );
}

export default Homepage;
