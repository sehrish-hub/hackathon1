import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Chapter 1: Introduction to Physical AI',
      link: {
        type: 'doc',
        id: 'intro/ch1-intro-physical-ai',
      },
      items: [
        'intro/topic-1-intro-to-physical-ai',
        'intro/topic-2-definition-and-historical-context',
        'intro/topic-3-why-humanoids-applications-challenges',
        'intro/topic-4-perception-decision-action-loop',
        'intro/topic-5-three-pillars-framework',
        // 'intro/topic-6-convergence-factors' removed: document does not exist
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: ROS 2: The Backbone of Physical AI',
      link: {
        type: 'doc',
        id: 'ros2-basics/ch2-ros2-basics',
      },
      items: [
        'ros2-basics/topic-1-evolution-from-ros1',
        'ros2-basics/topic-2-ros2-architecture',
        'ros2-basics/topic-3-nodes-modular-components',
        'ros2-basics/topic-4-topics-realtime-data',
        'ros2-basics/topic-5-services-actions',
        // 'ros2-basics/topic-6-ros2-in-physical-ai' removed: document does not exist
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
