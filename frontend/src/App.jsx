import { useState } from 'react'
import {
  Container,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Link,
  CircularProgress,
  Box,
  Paper
} from '@mui/material'

function App() {
  const [items, setItems] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(false)
  const [scraped, setScraped] = useState(false)

  const refreshProducts = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/refresh`)
      const { message } = await res.json()
      console.log(message)

      const productsRes = await fetch(`${import.meta.env.VITE_API_URL}/products`)
      const data = await productsRes.json()
      setItems(data)
      setScraped(true)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const filtered = items.filter((p) =>
    `${p.brand} ${p.name}`.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#f3f4f6' }}>
      {/* Header */}
      <Box
        sx={{
          py: 4,
          background: 'linear-gradient(90deg, #1976d2, #42a5f5)',
          color: '#fff',
          mb: 4,
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="h3" fontWeight="bold" textAlign="center">
            🛍️ Myntra Product Scraper
          </Typography>
          <Typography textAlign="center" sx={{ mt: 1 }}>
            Scrape and browse latest items directly from Myntra
          </Typography>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxWidth="lg">
        <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
          <Grid container spacing={2} alignItems="center" justifyContent="center">
            <Grid item xs={12} md={6}>
              <TextField
                label="Search by brand or product"
                variant="outlined"
                fullWidth
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                disabled={!scraped}
              />
            </Grid>
            <Grid item xs="auto">
              <Button
                variant="contained"
                color="primary"
                onClick={refreshProducts}
                disabled={loading}
                size="large"
              >
                {loading ? 'Scraping…' : 'Scrape Products'}
              </Button>
            </Grid>
          </Grid>
        </Paper>

        {loading && (
          <Grid container justifyContent="center" sx={{ my: 6 }}>
            <CircularProgress size={50} />
          </Grid>
        )}

        {!loading && scraped && filtered.length === 0 && (
          <Typography align="center" color="text.secondary">
            No products found.
          </Typography>
        )}

        {!loading && scraped && filtered.length > 0 && (
          <Grid container spacing={4}>
            {filtered.map((p, i) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={i}>
                <Card elevation={4} sx={{ borderRadius: 3 }}>
                  <CardMedia
                    component="img"
                    height="220"
                    image={p.image}
                    alt={p.name}
                    sx={{ objectFit: 'cover' }}
                  />
                  <CardContent>
                    <Link
                      href={p.link}
                      target="_blank"
                      rel="noreferrer"
                      underline="hover"
                      color="primary"
                      variant="subtitle1"
                      display="block"
                      fontWeight="bold"
                    >
                      {p.brand} – {p.name}
                    </Link>
                    <Typography variant="body2" color="text.secondary">
                      Price: {p.price}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Container>
    </Box>
  )
}

export default App
