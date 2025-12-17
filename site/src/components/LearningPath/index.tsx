import type { ReactNode } from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

export default function LearningPath(): ReactNode {
  const learningStages = [
    {
      title: "Foundations",
      description: "Core principles of physical artificial intelligence and embodied cognition",
    },
    {
      title: "Perception",
      description: "Sensory processing, computer vision, and sensor fusion techniques",
    },
    {
      title: "World Modeling",
      description: "Representing and understanding the physical environment",
    },
    {
      title: "Planning & Control",
      description: "Motion planning, trajectory generation, and control systems",
    },
    {
      title: "Autonomy",
      description: "Decision making, behavioral patterns, and goal-oriented systems",
    },
    {
      title: "Sim-to-Real",
      description: "Bridging simulation and real-world deployment challenges",
    },
  ];

  return (
    <section className={styles.learningPathSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Learning Path</h2>
        <div className={styles.pathContainer} role="list">
          {learningStages.map((stage, index) => (
            <div
              key={index}
              className={clsx(styles.pathStep, styles.pathItem)}
              role="listitem"
            >
              <div className={styles.stepNumber}>
                <span className={styles.number}>{index + 1}</span>
              </div>
              <div className={styles.stepContent}>
                <h3 className={styles.stepTitle}>{stage.title}</h3>
                <p className={styles.stepDescription}>{stage.description}</p>
              </div>
              {index < learningStages.length - 1 && (
                <div className={styles.pathArrow} aria-hidden="true">→</div>
              )}
            </div>
          ))}
        </div>

        <div className={styles.targetAudience}>
          <h3 className={styles.audienceTitle}>Who This Book Is For</h3>
          <ul className={styles.audienceList}>
            <li className={styles.audienceItem}>Robotics Engineers & Researchers</li>
            <li className={styles.audienceItem}>AI/ML Engineers working on embodied systems</li>
            <li className={styles.audienceItem}>Computer Vision & Perception Specialists</li>
            <li className={styles.audienceItem}>Advanced Students in Robotics & AI</li>
            <li className={styles.audienceItem}>System Architects building robotic applications</li>
          </ul>
          <p className={styles.audienceNote}>
            <strong>Note:</strong> This book is designed for technical practitioners,
            not for casual readers or those seeking high-level overviews.
          </p>
        </div>
      </div>
    </section>
  );
}