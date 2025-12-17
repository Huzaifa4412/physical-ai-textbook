import type { ReactNode } from "react";
import clsx from "clsx";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";
import Heading from "@theme/Heading";
import HeroSection from "@site/src/components/HeroSection";
import FeaturesSection from "@site/src/components/FeaturesSection";
import CoreTopicsSection from "@site/src/components/CoreTopicsSection";
import LearningPath from "@site/src/components/LearningPath";

import styles from "./index.module.css";
import cardsStyles from "../css/cards.module.css";

export default function Home(): ReactNode {
	const { siteConfig } = useDocusaurusContext();
	return (
		<Layout
			title={`Physical AI & Humanoid Systems - ${siteConfig.title}`}
			description="A deep, engineering-focused guide to embodied intelligence, humanoid robots, perception, control, and real-world AI systems"
		>
			<HeroSection />
			<FeaturesSection />
			<CoreTopicsSection />
			<LearningPath />
			<main>
				<HomepageFeatures />
			</main>
		</Layout>
	);
}
