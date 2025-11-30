import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Embodied Intelligence',
    description: (
      <>
        Explore how AI is moving beyond the screen, empowering robots to perceive, reason, and act within the physical world, fostering true embodied intelligence.
      </>
    ),
  },
  {
    title: 'Advanced Humanoid Robotics',
    description: (
      <>
        Delve into the cutting-edge of humanoid design, locomotion, and manipulation, understanding how these machines are built to navigate and interact with human-centric environments.
      </>
    ),
  },
  {
    title: 'ROS 2 & LLM Integration',
    description: (
      <>
        Learn about the powerful synergy between ROS 2, the Robot Operating System, and Large Language Models (LLMs) to create intelligent, adaptable, and human-friendly robotic systems.
      </>
    ),
  },
];

function Feature({title, description}: FeatureItem) {
  let imageSrc;
  let altText;
  if (title === 'Embodied Intelligence') {
    imageSrc = '/img/robot_head.svg';
    altText = 'Embodied Intelligence Icon';
  } else if (title === 'Advanced Humanoid Robotics') {
    imageSrc = '/img/humanoid_robot.svg';
    altText = 'Humanoid Robot Icon';
  } else if (title === 'ROS 2 & LLM Integration') {
    imageSrc = '/img/integration.svg';
    altText = 'Integration Icon';
  }

  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        {imageSrc && <img src={imageSrc} alt={altText} className={styles.featureSvg} />}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
