import { useEffect, useState } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'
const VALID_CHARS = /^[ACGTacgt\s]*$/
const DEBOUNCE_MS = 400

function App() {
  const [sequence, setSequence] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const hasOnlyValidChars = VALID_CHARS.test(sequence)
  const rawLength = sequence.length
  const cleanLength = sequence.replace(/\s/g, '').length

  useEffect(() => {
    if (sequence.trim() === '') {
      setResult(null)
      setError(null)
      return
    }

    const timeoutId = setTimeout(() => {
      fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sequence }),
      })
        .then((res) => res.json())
        .then((data) => {
          setResult(data)
          setError(null)
        })
        .catch(() => {
          setError('Could not reach the server')
          setResult(null)
        })
    }, DEBOUNCE_MS)

    return () => clearTimeout(timeoutId)
  }, [sequence])

  function handleFileUpload(event) {
    const file = event.target.files[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = () => {
      const text = reader.result
      const withoutHeader = text
        .split('\n')
        .filter((line) => !line.startsWith('>'))
        .join('\n')
      setSequence(withoutHeader)
    }
    reader.readAsText(file)
  }

  return (
    <section id="analyzer">
      <h1>Genome Sequence Analyzer</h1>

      <textarea
        value={sequence}
        onChange={(event) => setSequence(event.target.value)}
        placeholder="Paste a DNA sequence (A, T, G, C)..."
        rows={6}
        className={hasOnlyValidChars ? 'valid' : 'invalid'}
      />

      <div className="controls">
        <label htmlFor="fasta-upload">Upload FASTA file:</label>
        <input id="fasta-upload" type="file" accept=".fasta,.fa,.txt" onChange={handleFileUpload} />
      </div>

      <div className="counters">
        <span>Raw length: {rawLength}</span>
        <span>Clean length: {cleanLength}</span>
        <span className={hasOnlyValidChars ? 'status-ok' : 'status-bad'}>
          {hasOnlyValidChars ? 'Characters look valid' : 'Unexpected characters detected'}
        </span>
      </div>

      {error && <p className="status-bad">{error}</p>}

      {result && (
        <div className="results">
          {result.is_valid ? (
            <ul>
              <li>Clean sequence: {result.clean_sequence}</li>
              <li>Length: {result.length}</li>
              <li>GC content: {result.gc_content_pct}%</li>
              <li>Reverse: {result.reverse}</li>
              <li>Complement: {result.complement}</li>
              <li>Reverse complement: {result.reverse_complement}</li>
            </ul>
          ) : (
            <p className="status-bad">{result.error}</p>
          )}
        </div>
      )}
    </section>
  )
}

export default App
