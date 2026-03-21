// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://mtpontes.github.io',
	base: '/workstate',
	integrations: [
		starlight({
			title: 'Workstate',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/mtpontes/workstate' },
			],
			sidebar: [
				{
					label: 'Fundamentos',
					items: [
						{ label: 'O Que é Capturado', slug: 'fundamentos/o-que-e-capturado' },
					],
				},
				{
					label: 'Guias',
					items: [
						{ label: 'Instalação', slug: 'guides/installation' },
						{ label: 'Configuração AWS', slug: 'guides/aws-setup' },
						{ label: 'Guia Rápido', slug: 'guides/quickstart' },
					],
				},
				{
					label: 'Referência',
					items: [
						{ label: 'Visão Geral', slug: 'reference/overview' },
						{
							label: 'Comandos',
							autogenerate: { directory: 'reference/commands' },
						},
					],
				},
				{
					label: 'Avançado',
					items: [
						{ label: 'Hooks e Automação', slug: 'avancado/hooks' },
						{ label: 'Desenvolvimento', slug: 'avancado/desenvolvimento' },
					],
				},
			],
		}),
	],
});
