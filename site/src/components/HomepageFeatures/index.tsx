import type { ReactNode } from "react";
import clsx from "clsx";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

type FeatureItem = {
	title: string;
	icon: string;
	description: ReactNode;
};

const FeatureList: FeatureItem[] = [
	{
		title: "Embodied Intelligence",
		icon: "🧠",
		description: (
			<>
				Deep dive into the principles of physical artificial intelligence
				and how AI systems can be embodied in real-world robotic platforms.
			</>
		),
	},
	{
		title: "Humanoid Control Systems",
		icon: "⚙️",
		description: (
			<>
				Comprehensive coverage of perception, planning, and control systems
				for humanoid robots, from sensors to actuators.
			</>
		),
	},
	{
		title: "Simulation & Deployment",
		icon: "🌐",
		description: (
			<>
				From digital twin simulation to real-world deployment,
				understanding the complete lifecycle of physical AI systems.
			</>
		),
	},
];

function Feature({ title, icon, description }: FeatureItem) {
	return (
		<div className={styles.featureItem}>
			<div className={styles.featureIcon}>
				<span className={styles.icon}>{icon}</span>
			</div>
			<div className={styles.featureContent}>
				<Heading as='h3'>{title}</Heading>
				<p>{description}</p>
			</div>
		</div>
	);
}

export default function HomepageFeatures(): ReactNode {
	return (
		<section className={styles.features}>
			<div className="container">
				<div className={styles.featuresGrid}>
					{FeatureList.map((props, idx) => (
						<Feature key={idx} {...props} />
					))}
				</div>
			</div>
		</section>
	);
}
