"use client"

import { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Play, ArrowLeft, Settings, Database } from "lucide-react"
import Link from "next/link"

export default function NewTraining() {
  const [progress, setProgress] = useState(0)
  const [epochs, setEpochs] = useState([100])
  const [batchSize, setBatchSize] = useState([16])
  const [imageSize, setImageSize] = useState([640])
  const [status, setStatus] = useState<"idle" | "running" | "completed" | "failed">(
    "idle",
  )
  const pollRef = useRef<NodeJS.Timeout | null>(null)

  const handleStartTraining = async () => {
    setStatus("running")
    setProgress(0)

    const config = {
      mode: "train",
      model: "yolov8n.pt",
      data: "/path/to/data.yaml",
      output: "/tmp/output",
      epochs: epochs[0],
      batch: batchSize[0],
      imgsz: imageSize[0],
    }

    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch("/api/status")
        const data = await res.json()
        const session = data.processes?.[0]
        if (session) {
          setProgress(session.progress || 0)
          if (session.status === "completed" || session.status === "failed") {
            clearInterval(pollRef.current as NodeJS.Timeout)
            setStatus(session.status === "completed" ? "completed" : "failed")
          }
        }
      } catch (e) {
        clearInterval(pollRef.current as NodeJS.Timeout)
        setStatus("failed")
      }
    }, 1000)

    try {
      const res = await fetch("/api/scripts", {
        method: "POST",
        body: JSON.stringify({ script: "run_yolo.py", action: "train", config }),
      })
      const result = await res.json()
      if (!res.ok || !result.success) {
        setStatus("failed")
      } else {
        setStatus("completed")
        setProgress(100)
      }
    } catch (error) {
      setStatus("failed")
    } finally {
      if (pollRef.current) clearInterval(pollRef.current)
    }
  }

  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current)
    }
  }, [])

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
            <h1 className="text-3xl font-bold">Start New Training</h1>
            <p className="text-muted-foreground">Configure and launch a YOLOv8 training session</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Configuration */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5" />
                  Dataset Configuration
                </CardTitle>
                <CardDescription>Select your dataset and model configuration</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="model">Base Model</Label>
                    <Select defaultValue="yolov8n">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="yolov8n">YOLOv8n (Nano)</SelectItem>
                        <SelectItem value="yolov8s">YOLOv8s (Small)</SelectItem>
                        <SelectItem value="yolov8m">YOLOv8m (Medium)</SelectItem>
                        <SelectItem value="yolov8l">YOLOv8l (Large)</SelectItem>
                        <SelectItem value="yolov8x">YOLOv8x (Extra Large)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="dataset">Dataset</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select dataset" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="construction">Construction Equipment</SelectItem>
                        <SelectItem value="vehicles">Vehicle Detection</SelectItem>
                        <SelectItem value="safety">Safety Equipment</SelectItem>
                        <SelectItem value="custom">Custom Dataset</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="data-yaml">Data YAML Path</Label>
                  <Input id="data-yaml" placeholder="/path/to/data.yaml" />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="output">Output Directory</Label>
                  <Input id="output" placeholder="/path/to/training/output" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Training Parameters
                </CardTitle>
                <CardDescription>Fine-tune your training hyperparameters</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label>Epochs</Label>
                      <span className="text-sm text-muted-foreground">{epochs[0]}</span>
                    </div>
                    <Slider value={epochs} onValueChange={setEpochs} max={300} min={10} step={10} className="w-full" />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label>Batch Size</Label>
                      <span className="text-sm text-muted-foreground">{batchSize[0]}</span>
                    </div>
                    <Slider
                      value={batchSize}
                      onValueChange={setBatchSize}
                      max={64}
                      min={1}
                      step={1}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label>Image Size</Label>
                      <span className="text-sm text-muted-foreground">{imageSize[0]}px</span>
                    </div>
                    <Slider
                      value={imageSize}
                      onValueChange={setImageSize}
                      max={1280}
                      min={320}
                      step={32}
                      className="w-full"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="learning-rate">Learning Rate</Label>
                    <Input id="learning-rate" placeholder="0.01" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="weight-decay">Weight Decay</Label>
                    <Input id="weight-decay" placeholder="0.0005" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Status & Actions */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Training Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {status === "running" ? (
                  <div className="space-y-4">
                    <div className="flex justify-between text-sm">
                      <span>Training in progress...</span>
                      <span>
                        Epoch {Math.floor((progress * epochs[0]) / 100)}/{epochs[0]}
                      </span>
                    </div>
                    <Progress value={progress} />
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <span className="text-muted-foreground">Loss:</span>
                        <span className="ml-2 font-mono">0.0234</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">mAP:</span>
                        <span className="ml-2 font-mono">0.847</span>
                      </div>
                    </div>
                    <Badge variant="outline" className="bg-blue-50 text-blue-700">
                      Training Active
                    </Badge>
                  </div>
                ) : status === "completed" ? (
                  <div className="space-y-3">
                    <Badge variant="outline" className="bg-green-50 text-green-700">
                      Training Complete
                    </Badge>
                  </div>
                ) : status === "failed" ? (
                  <div className="space-y-3">
                    <Badge variant="destructive">Training Failed</Badge>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <Badge variant="outline" className="bg-green-50 text-green-700">
                      Ready to Train
                    </Badge>
                    <p className="text-sm text-muted-foreground">Configure your parameters and start training.</p>
                  </div>
                )}

                <Button
                  className="w-full bg-purple-600 hover:bg-purple-700"
                  onClick={handleStartTraining}
                  disabled={status === "running"}
                >
                  <Play className="h-4 w-4 mr-2" />
                  {status === "running" ? "Training..." : "Start Training"}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>System Resources</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>GPU Memory</span>
                    <span>6.2GB / 8GB</span>
                  </div>
                  <Progress value={77} />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>CPU Usage</span>
                    <span>45%</span>
                  </div>
                  <Progress value={45} />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>RAM Usage</span>
                    <span>12.4GB / 32GB</span>
                  </div>
                  <Progress value={39} />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Recent Training Sessions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    { name: "construction_v2", epochs: "100/100", status: "completed", time: "2 hours ago" },
                    { name: "vehicles_yolov8s", epochs: "75/100", status: "failed", time: "1 day ago" },
                    { name: "safety_equipment", epochs: "100/100", status: "completed", time: "3 days ago" },
                  ].map((item, index) => (
                    <div key={index} className="flex justify-between items-center p-3 rounded-lg bg-slate-50">
                      <div>
                        <p className="font-medium">{item.name}</p>
                        <p className="text-sm text-muted-foreground">{item.epochs} epochs</p>
                      </div>
                      <div className="text-right">
                        <Badge variant={item.status === "completed" ? "default" : "destructive"}>{item.status}</Badge>
                        <p className="text-sm text-muted-foreground mt-1">{item.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
