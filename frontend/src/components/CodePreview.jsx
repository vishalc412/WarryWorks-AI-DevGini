import React from 'react'
import { Download, Copy } from 'lucide-react'

const CodePreview = ({ artifact }) => {
  const handleCopy = () => {
    navigator.clipboard.writeText(artifact.content || '')
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">{artifact.name}</h2>
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="btn btn-secondary flex items-center gap-2"
          >
            <Copy className="w-4 h-4" />
            Copy
          </button>
          <button className="btn btn-secondary flex items-center gap-2">
            <Download className="w-4 h-4" />
            Download
          </button>
        </div>
      </div>

      <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
        <pre className="text-sm text-gray-100">
          <code>{artifact.content || 'No content available'}</code>
        </pre>
      </div>
    </div>
  )
}

export default CodePreview
