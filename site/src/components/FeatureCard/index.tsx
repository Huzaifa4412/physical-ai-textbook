import type { ReactNode } from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

interface FeatureCardProps {
  title: string;
  description: string;
  icon?: string;
}

export default function FeatureCard({ title, description, icon }: FeatureCardProps): ReactNode {
  return (
    <div className={clsx(styles.card, "padding--lg")}>
      {icon && (
        <div className={styles.icon} aria-hidden="true">
          {icon}
        </div>
      )}
      <h3 className={clsx(styles.cardTitle, "text--center")}>
        {title}
      </h3>
      <p className={clsx(styles.cardDescription, "text--center")}>
        {description}
      </p>
    </div>
  );
}