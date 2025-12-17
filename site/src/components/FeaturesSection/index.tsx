import type { ReactNode } from "react";
import clsx from "clsx";
import FeatureCard from "@site/src/components/FeatureCard";
import styles from "./styles.module.css";

export default function FeaturesSection(): ReactNode {
  const features = [
    {
      title: "Physical AI First",
      description: "Intelligence grounded in physics and embodiment",
      icon: "🤖",
    },
    {
      title: "Humanoid Systems",
      description: "Robot brains, perception, locomotion, manipulation",
      icon: "🦾",
    },
    {
      title: "Simulation → Reality",
      description: "Digital twins, sim-to-real transfer",
      icon: "🔄",
    },
    {
      title: "Systems Thinking",
      description: "End-to-end pipelines, not isolated models",
      icon: "🔗",
    },
  ];

  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <div className={styles.grid}>
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              title={feature.title}
              description={feature.description}
              icon={feature.icon}
            />
          ))}
        </div>
      </div>
    </section>
  );
}