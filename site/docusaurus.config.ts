import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
	title: "Physical-ai-humanoid-robotics",
	tagline:
		"Explore the future of robotics with our comprehensive course on Physical AI & Humanoid Robotics. Learn how AI systems bridge the digital and physical worlds, enabling humanoid robots to interact naturally in human environments. This book covers ROS 2, Gazebo, Unity, NVIDIA Isaac, and advanced AI integration, providing students and professionals with practical skills for the next generation of robotics.",
	favicon: "img/favicon.ico",

	// Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
	future: {
		v4: true, // Improve compatibility with the upcoming Docusaurus v4
	},

	// Set the production url of your site here
	url: "https://physical-ai-textbook-woad.vercel.app/",
	// Set the /<baseUrl>/ pathname under which your site is served
	// For GitHub pages deployment, it is often '/<projectName>/'
	baseUrl: "/",

	// GitHub pages deployment config.
	// If you aren't using GitHub pages, you don't need these.
	organizationName: "facebook", // Usually your GitHub org/user name.
	projectName: "docusaurus", // Usually your repo name.

	onBrokenLinks: "throw",

	// Even if you don't use internationalization, you can use this field to set
	// useful metadata like html lang. For example, if your site is Chinese, you
	// may want to replace "en" with "zh-Hans".
	i18n: {
		defaultLocale: "en",
		locales: ["en"],
	},

	presets: [
		[
			"classic",
			{
				docs: {
					sidebarPath: "./sidebars.ts",
					// Please change this to your repo.
					// Remove this to remove the "edit this page" links.
					editUrl:
						"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/",
				},

				theme: {
					customCss: "./src/css/custom.css",
				},
			} satisfies Preset.Options,
		],
	],

	themeConfig: {
		// Replace with your project's social card
		image: "img/docusaurus-social-card.jpg",
		colorMode: {
			respectPrefersColorScheme: true,
		},
		navbar: {
			title: "Physical AI & Humanoid Systems",
			logo: {
				alt: "Physical AI & Humanoid Systems Logo",
				src: "img/logo.svg",
			},
			items: [
				{
					type: "doc",
					position: "left",
					label: "Docs",
					docId: "/category/introduction",
				},
				{
					to: "/docs/category/introduction",
					position: "left",
					label: "Book Structure",
				},
				{
					href: "https://github.com/Huzaifa4412/physical-ai-textbook",
					label: "GitHub",
					position: "right",
				},
			],
		},
		footer: {
			style: "dark",
			links: [
				{
					title: "Learn",
					items: [
						{
							label: "Introduction",
							to: "/docs/category/introduction",
						},
						{
							label: "Physical AI Fundamentals",
							to: "/docs/book-introduction/physical-ai-embodied-intelligence",
						},
						{
							label: "Robot Brain Architecture",
							to: "/docs/category/the-ai-robot-brain-nvidia-isaac",
						},
						{
							label: "Digital Twins & Simulation",
							to: "/docs/category/the-digital-twin-gazebo--unity",
						},
						{
							label: "ROS2 Nervous System",
							to: "/docs/category/the-robotic-nervous-system-ros-2",
						},
					],
				},
				{
					title: "Resources",
					items: [
						{
							label: "Book Structure",
							to: "/docs/category/introduction",
						},
						{
							label: "GitHub Repository",
							href: "https://github.com/Huzaifa4412/physical-ai-textbook",
						},
						{
							label: "NVIDIA Isaac Documentation",
							href: "https://nvidia-isaac-ros.github.io/",
						},
						{
							label: "ROS2 Documentation",
							href: "https://docs.ros.org/en/humble/",
						},
					],
				},
				{
					title: "Community",
					items: [
						{
							label: "GitHub",
							href: "https://github.com/Huzaifa4412/physical-ai-textbook",
						},
						{
							label: "Discord",
							href: "https://discordapp.com/invite/docusaurus",
						},
						{
							label: "Twitter",
							href: "https://twitter.com",
						},
						{
							label: "LinkedIn",
							href: "https://linkedin.com",
						},
					],
				},
				{
					title: "More",
					items: [
						{
							label: "Author Website",
							to: "https://huzaifa-mukhtar-official.vercel.app/",
						},
						{
							label: "Docusaurus",
							href: "https://docusaurus.io",
						},
						{
							label: "Privacy Policy",
							to: "/privacy",
						},
						{
							label: "Terms of Service",
							to: "/terms",
						},
					],
				},
			],
			copyright: `Copyright © ${new Date().getFullYear()} Huzaifa Mukhtar. Physical AI & Humanoid Systems. Built with Docusaurus.`,
		},
		prism: {
			theme: prismThemes.github,
			darkTheme: prismThemes.dracula,
		},
	} satisfies Preset.ThemeConfig,
};

export default config;
