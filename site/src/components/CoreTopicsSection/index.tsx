import type { ReactNode } from "react";
import clsx from "clsx";
import BentoGrid from "@site/src/components/BentoGrid";
import styles from "./styles.module.css";

export default function CoreTopicsSection(): ReactNode {
  const coreTopics = [
    {
      title: "Robot Brain Architecture",
      description: "Core architectural patterns for intelligent robotic systems",
    },
    {
      title: "Perception & Sensor Fusion",
      description: "Processing sensory data from multiple modalities",
    },
    {
      title: "Planning & Control",
      description: "Motion planning and control algorithms",
    },
    {
      title: "ROS2 Nervous System",
      description: "Communication frameworks for robotic applications",
    },
    {
      title: "Digital Twins",
      description: "Virtual models for simulation and testing",
    },
    {
      title: "Autonomy & Behavior",
      description: "Decision making and behavioral patterns",
    },
  ];

  return (
    <section className={styles.coreTopicsSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Core Topics</h2>
        <BentoGrid items={coreTopics} />
      </div>
    </section>
  );
}