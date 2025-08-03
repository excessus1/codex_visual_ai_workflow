"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Camera, Play, ArrowLeft, Upload, Download, Eye } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function ImagePrediction() {
  const [isPredicting, setIsPredicting] = useState(false)
  const [progress, setProgress] = useState(0)
  const [confidence, setConfidence] = useState([0.25])
  const [selectedImage, setSelectedImage] = useState<string | null>(null)

  const handlePredict = async () => {
    setIsPredicting(true)
    setProgress(0)

    // Simulate prediction progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsPredicting(false)
          return 100
        }
        return prev + 20
      })
    }, 300)
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
            <h1 className="text-3xl font-bold">Image Prediction</h1>
            <p className="text-muted-foreground">Run object detection on images using trained models</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Configuration */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Camera className="h-5 w-5" />
                  Input Configuration
                </CardTitle>
                <CardDescription>Select images and model for prediction</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="model">Model</Label>
                    <Select defaultValue="construction_v2">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="construction_v2">Construction Equipment v2</SelectItem>
                        <SelectItem value="vehicles_yolov8s">Vehicle Detection</SelectItem>
                        <SelectItem value="safety_equipment">Safety Equipment</SelectItem>
                        <SelectItem value="yolov8n">YOLOv8n (Base)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="source">Source Type</Label>
                    <Select defaultValue="directory">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="directory">Directory</SelectItem>
                        <SelectItem value="single">Single Image</SelectItem>
                        <SelectItem value="upload">Upload Images</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="source-path">Source Path</Label>
                  <div className="flex gap-2">
                    <Input id="source-path" placeholder="/path/to/images" />
                    <Button variant="outline">
                      <Upload className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="output">Output Directory</Label>
                  <Input id="output" placeholder="/path/to/predictions" />
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label>Confidence Threshold</Label>
                    <span className="text-sm text-muted-foreground">{confidence[0]}</span>
                  </div>
                  <Slider
                    value={confidence}
                    onValueChange={setConfidence}
                    max={1}
                    min={0.1}
                    step={0.05}
                    className="w-full"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Preview */}
            <Card>
              <CardHeader>
                <CardTitle>Image Preview</CardTitle>
                <CardDescription>Preview selected images and predictions</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {[1, 2, 3, 4, 5, 6].map((i) => (
                    <div
                      key={i}
                      className="relative aspect-square rounded-lg overflow-hidden bg-slate-100 cursor-pointer hover:ring-2 hover:ring-blue-500"
                    >
                      <Image
                        src={`/placeholder-4vbgw.png?height=200&width=200&text=Image ${i}`}
                        alt={`Preview ${i}`}
                        fill
                        className="object-cover"
                      />
                      <div className="absolute inset-0 bg-black/0 hover:bg-black/10 transition-colors flex items-center justify-center">
                        <Eye className="h-6 w-6 text-white opacity-0 hover:opacity-100 transition-opacity" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Status & Actions */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Prediction Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {isPredicting ? (
                  <div className="space-y-4">
                    <div className="flex justify-between text-sm">
                      <span>Processing images...</span>
                      <span>{progress}%</span>
                    </div>
                    <Progress value={progress} />
                    <div className="text-sm">
                      <span className="text-muted-foreground">Current:</span>
                      <span className="ml-2 font-mono">image_045.jpg</span>
                    </div>
                    <Badge variant="outline" className="bg-blue-50 text-blue-700">
                      Predicting
                    </Badge>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <Badge variant="outline" className="bg-green-50 text-green-700">
                      Ready to Predict
                    </Badge>
                    <p className="text-sm text-muted-foreground">Configure your settings and start prediction.</p>
                  </div>
                )}

                <Button
                  className="w-full bg-yellow-600 hover:bg-yellow-700"
                  onClick={handlePredict}
                  disabled={isPredicting}
                >
                  <Play className="h-4 w-4 mr-2" />
                  {isPredicting ? "Predicting..." : "Start Prediction"}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Prediction Results</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Images Processed</span>
                    <Badge variant="outline">247</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Objects Detected</span>
                    <Badge variant="outline">1,234</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Average Confidence</span>
                    <Badge variant="outline">0.87</Badge>
                  </div>
                </div>

                <Button variant="outline" className="w-full bg-transparent">
                  <Download className="h-4 w-4 mr-2" />
                  Download Results
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Detection Classes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {[
                    { name: "Excavator", count: 45, confidence: 0.92 },
                    { name: "Bulldozer", count: 23, confidence: 0.88 },
                    { name: "Crane", count: 12, confidence: 0.85 },
                    { name: "Dump Truck", count: 67, confidence: 0.91 },
                  ].map((item, index) => (
                    <div key={index} className="flex justify-between items-center p-2 rounded bg-slate-50">
                      <div>
                        <p className="font-medium text-sm">{item.name}</p>
                        <p className="text-xs text-muted-foreground">Conf: {item.confidence}</p>
                      </div>
                      <Badge variant="outline">{item.count}</Badge>
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
