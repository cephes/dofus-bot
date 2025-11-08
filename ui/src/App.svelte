<script>
  import { onMount } from 'svelte';

  let health = 'Loading...';

  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      health = JSON.stringify(data, null, 2);
    } catch (error) {
      health = `Error: ${error.message}`;
    }
  });
</script>

<main>
  <h1>Dofus Bot UI</h1>
  <h2>Orchestrator Health</h2>
  <pre>{health}</pre>
</main>

<style>
  main {
    font-family: Arial, sans-serif;
    padding: 20px;
  }
  h1 {
    color: #333;
  }
  pre {
    background: #f4f4f4;
    padding: 10px;
    border-radius: 4px;
  }
</style>