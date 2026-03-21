// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://mtpontes.github.io',
	base: '/workstate',
	devToolbar: {
		enabled: false,
	},
	integrations: [
		starlight({
			title: 'Workstate',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/mtpontes/workstate' },
			],
			defaultLocale: 'root',
			locales: {
				root: { label: 'English', lang: 'en' },
				'pt-br': { label: 'Português', lang: 'pt-BR' },
			},
			sidebar: [
				{
					label: 'Guides',
					items: [
						{ label: 'Installation', slug: 'guides/installation' },
						{ label: 'Quickstart', slug: 'guides/quickstart' },
						{ label: 'AWS Setup', slug: 'guides/aws-setup' },
					],
				},
				{
					label: 'Foundations',
					items: [
						{ label: 'What is Captured', slug: 'foundations/what-is-captured' },
					],
				},
				{
					label: 'Reference',
					items: [
						{ label: 'Commands Overview', slug: 'reference/overview' },
						{
							label: 'Commands',
							autogenerate: { directory: 'reference/commands' },
						},
					],
				},
				{
					label: 'Advanced',
					items: [
						{ label: 'Hooks and Automation', slug: 'avancado/hooks' },
						{ label: 'Development', slug: 'avancado/desenvolvimento' },
					],
				},
			],
		}),
	],
});
