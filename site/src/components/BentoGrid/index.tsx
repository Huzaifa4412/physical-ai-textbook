import type { ReactNode } from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

interface BentoGridItem {
  title: string;
  description?: string;
  icon?: string;
}

interface BentoGridProps {
  items: BentoGridItem[];
}

export default function BentoGrid({ items }: BentoGridProps): ReactNode {
  return (
    <section className={styles.bentoGridSection}>
      <div className="container">
        <div className={styles.bentoGrid}>
          {items.map((item, index) => (
            <div
              key={index}
              className={styles.bentoItem}
            >
              {item.icon && (
                <div className={styles.icon} aria-hidden="true">
                  {item.icon}
                </div>
              )}
              <h3 className={styles.bentoTitle}>{item.title}</h3>
              {item.description && (
                <p className={styles.bentoDescription}>{item.description}</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}