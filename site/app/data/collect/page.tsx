"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { FolderOpen, Plus, Trash2, ArrowLeft, Upload } from "lucide-react"
import Link from "next/link"
import { formatDistanceToNow } from "date-fns"

interface Dataset {
  id: number
  name: string
  image_count: number
  created_at: string
}

export default function CollectImages() {
  const [sources, setSources] = useState<string[]>([""])
  const [isRunning, setIsRunning] = useState(false)
  const [progress, setProgress] = useState(0)
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [isLoadingDatasets, setIsLoadingDatasets] = useState(true)

  useEffect(() => {
    const fetchDatasets = async () => {
      setIsLoadingDatasets(true)
      try {
        const res = await fetch("/api/datasets")
        const data: Dataset[] = await res.json()
        setDatasets(data)
      } catch (err) {
        console.error("Failed to fetch datasets:", err)
      } finally {
        setIsLoadingDatasets(false)
      }
    }
    fetchDatasets()
  }, [])

  const addSource = () => {
    setSources([...sources, ""])
  }

  const removeSource = (index: number) => {
    setSources(sources.filter((_, i) => i !== index))
  }

  const updateSource = (index: number, value: string) => {
    const newSources = [...sources]
    newSources[index] = value
    setSources(newSources)
  }

  const handleCollect = async () => {
    setIsRunning(true)
    setProgress(0)

    // Simulate progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsRunning(false)
          return 100
        }
        return prev + 10
      })
    }, 500)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/">
            <Button variant="outline" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold">Collect Images</h1>
            <p className="text-muted-foreground">Gather images from multiple sources into a unified dataset</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Configuration */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FolderOpen className="h-5 w-5" />
                  Source Directories
                </CardTitle>
                <CardDescription>Add directories containing images to collect</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {sources.map((source, index) => (
                  <div key={index} className="flex gap-2">
                    <Input
                      placeholder="/path/to/image/directory"
                      value={source}
                      onChange={(e) => updateSource(index, e.target.value)}
                    />
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => removeSource(index)}
                      disabled={sources.length === 1}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                <Button variant="outline" onClick={addSource} className="w-full bg-transparent">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Source Directory
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Collection Settings</CardTitle>
                <CardDescription>Configure how images are collected and organized</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="destination">Destination Directory</Label>
                    <Input id="destination" placeholder="/path/to/destination" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="rename-scheme">Rename Scheme</Label>
                    <Select defaultValue="source_prefix">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="source_prefix">Source Prefix</SelectItem>
                        <SelectItem value="timestamp_hash">Timestamp Hash</SelectItem>
                        <SelectItem value="sequential">Sequential</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="extensions">File Extensions</Label>
                  <Input id="extensions" placeholder=".jpg, .jpeg, .png" defaultValue=".jpg, .jpeg, .png" />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Rename Only on Conflict</Label>
                      <p className="text-sm text-muted-foreground">Only rename files when there's a naming conflict</p>
                    </div>
                    <Switch />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Delete Missing in Sources</Label>
                      <p className="text-sm text-muted-foreground">
                        Remove files from destination if not found in sources
                      </p>
                    </div>
                    <Switch />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Status & Actions */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Collection Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {isRunning ? (
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span>Collecting images...</span>
                      <span>{progress}%</span>
                    </div>
                    <Progress value={progress} />
                    <Badge variant="outline" className="bg-blue-50 text-blue-700">
                      Processing
                    </Badge>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <Badge variant="outline" className="bg-green-50 text-green-700">
                      Ready to Collect
                    </Badge>
                    <p className="text-sm text-muted-foreground">
                      Configure your sources and settings, then start collection.
                    </p>
                  </div>
                )}

                <Button className="w-full" onClick={handleCollect} disabled={isRunning}>
                  <Upload className="h-4 w-4 mr-2" />
                  {isRunning ? "Collecting..." : "Start Collection"}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Recent Collections</CardTitle>
              </CardHeader>
              <CardContent>
                {isLoadingDatasets ? (
                  <div className="text-center py-4 text-muted-foreground">Loading...</div>
                ) : datasets.length === 0 ? (
                  <div className="text-center py-4 text-muted-foreground">No collections yet</div>
                ) : (
                  <div className="space-y-3">
                    {datasets.map((item) => (
                      <div
                        key={item.id}
                        className="flex justify-between items-center p-3 rounded-lg bg-slate-50"
                      >
                        <div>
                          <p className="font-medium">{item.name}</p>
                          <p className="text-sm text-muted-foreground">{item.image_count} images</p>
                        </div>
                        <span className="text-sm text-muted-foreground">
                          {formatDistanceToNow(new Date(item.created_at), { addSuffix: true })}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
