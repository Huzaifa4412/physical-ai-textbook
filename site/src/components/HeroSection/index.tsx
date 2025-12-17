import type { ReactNode } from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import styles from "./styles.module.css";
import buttonsStyles from "@site/src/css/buttons.module.css";

interface HeroSectionProps {
  title?: string;
  subtitle?: string;
  supportingText?: string;
  primaryCtaText?: string;
  primaryCtaUrl?: string;
  secondaryCtaText?: string;
  secondaryCtaUrl?: string;
}

export default function HeroSection({
  title = "Physical AI & Humanoid Systems",
  subtitle = "embodied intelligence, robotics, real-world AI",
  supportingText = "Building the next generation of intelligent robotic systems",
  primaryCtaText = "Start Reading",
  primaryCtaUrl = "/docs/category/introduction",
  secondaryCtaText = "View Structure",
  secondaryCtaUrl = "/docs/category/introduction",
}: HeroSectionProps): ReactNode {
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent} role="banner">
          <div className={styles.textContent}>
            <div className={styles.badge}>Physical AI & Robotics</div>
            <h1 className={clsx("hero__title", styles.heroTitle)}>
              {title}
            </h1>
            <p className={clsx("hero__subtitle", styles.heroSubtitle)}>
              {subtitle}
            </p>
            {supportingText && (
              <p className={clsx(styles.heroSupportingText)}>
                {supportingText}
              </p>
            )}
            <div className={styles.heroButtons}>
              <Link
                className={buttonsStyles.primaryButton}
                to={primaryCtaUrl}
                aria-label={`Navigate to ${primaryCtaText}`}
              >
                {primaryCtaText}
              </Link>
              <Link
                className={buttonsStyles.secondaryButton}
                to={secondaryCtaUrl}
                aria-label={`Navigate to ${secondaryCtaText}`}
              >
                {secondaryCtaText}
              </Link>
            </div>
            <div className={styles.stats}>
              <div className={styles.statItem}>
                <span className={styles.statNumber}>50+</span>
                <span className={styles.statLabel}>Concepts</span>
              </div>
              <div className={styles.statItem}>
                <span className={styles.statNumber}>200+</span>
                <span className={styles.statLabel}>Examples</span>
              </div>
              <div className={styles.statItem}>
                <span className={styles.statNumber}>10+</span>
                <span className={styles.statLabel}>Projects</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}