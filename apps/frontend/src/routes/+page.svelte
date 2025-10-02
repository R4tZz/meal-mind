<script lang="ts">
	import { onMount } from 'svelte';
	
	let apiStatus = 'Loading...';
	let dbStatus = 'Loading...';
	let apiMessage = '';
	let dbMessage = '';
	
	onMount(async () => {
		// Test API health endpoint
		try {
			const apiResponse = await fetch('http://localhost:8000/health');
			const apiData = await apiResponse.json();
			apiStatus = apiData.status;
			apiMessage = 'API is reachable from frontend!';
		} catch (error) {
			apiStatus = 'error';
			apiMessage = `Error: ${error}`;
		}
		
		// Test database connection endpoint
		try {
			const dbResponse = await fetch('http://localhost:8000/db-test');
			const dbData = await dbResponse.json();
			dbStatus = dbData.status;
			dbMessage = dbData.message;
		} catch (error) {
			dbStatus = 'error';
			dbMessage = `Error: ${error}`;
		}
	});
</script>

<h1>Welcome to MealMind</h1>
<p>Testing container communication...</p>

<div class="status-container">
	<h2>Frontend → Backend Communication</h2>
	<p>Status: <strong class:healthy={apiStatus === 'healthy'} class:error={apiStatus === 'error'}>{apiStatus}</strong></p>
	<p>{apiMessage}</p>
</div>

<div class="status-container">
	<h2>Backend → Database Communication</h2>
	<p>Status: <strong class:healthy={dbStatus === 'success'} class:error={dbStatus === 'error'}>{dbStatus}</strong></p>
	<p>{dbMessage}</p>
</div>

<style>
	.status-container {
		margin: 2rem 0;
		padding: 1rem;
		border: 1px solid #ccc;
		border-radius: 8px;
	}
	
	.healthy {
		color: green;
	}
	
	.error {
		color: red;
	}
</style>
