import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Brain, Camera, Database, FileImage, Play, Settings, Upload, Video, Zap } from "lucide-react"
import Link from "next/link"

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold">Visual AI Workflow</h1>
                <p className="text-sm text-muted-foreground">YOLOv8 Training & Prediction Platform</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                System Ready
              </Badge>
              <Button variant="outline" size="sm">
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Images</p>
                  <p className="text-2xl font-bold">2,847</p>
                </div>
                <FileImage className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Models Trained</p>
                  <p className="text-2xl font-bold">12</p>
                </div>
                <Brain className="h-8 w-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Predictions Run</p>
                  <p className="text-2xl font-bold">156</p>
                </div>
                <Zap className="h-8 w-8 text-yellow-600" />
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Active Jobs</p>
                  <p className="text-2xl font-bold">3</p>
                </div>
                <Play className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Current Training Status */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Play className="h-5 w-5 text-green-600" />
              Current Training Session
            </CardTitle>
            <CardDescription>Training YOLOv8 model on construction equipment dataset</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between text-sm">
                <span>Epoch 45/100</span>
                <span>ETA: 2h 15m</span>
              </div>
              <Progress value={45} className="h-2" />
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Loss:</span>
                  <span className="ml-2 font-mono">0.0234</span>
                </div>
                <div>
                  <span className="text-muted-foreground">mAP@0.5:</span>
                  <span className="ml-2 font-mono">0.847</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Precision:</span>
                  <span className="ml-2 font-mono">0.892</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Workflow Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Data Management */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5 text-blue-600" />
                Data Management
              </CardTitle>
              <CardDescription>Collect, organize, and prepare your image datasets</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Link href="/data/collect">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    <Upload className="h-4 w-4 mr-2" />
                    Collect Images
                  </Button>
                </Link>
                <Link href="/data/organize">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    <FileImage className="h-4 w-4 mr-2" />
                    Organize Dataset
                  </Button>
                </Link>
                <Link href="/data/annotate">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    <Settings className="h-4 w-4 mr-2" />
                    Annotation Tools
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Training */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5 text-purple-600" />
                Model Training
              </CardTitle>
              <CardDescription>Train YOLOv8 models on your custom datasets</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Link href="/training/new">
                  <Button className="w-full justify-start bg-purple-600 hover:bg-purple-700">
                    <Play className="h-4 w-4 mr-2" />
                    Start Training
                  </Button>
                </Link>
                <Link href="/training/history">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    <Database className="h-4 w-4 mr-2" />
                    Training History
                  </Button>
                </Link>
                <Link href="/models">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    <Settings className="h-4 w-4 mr-2" />
                    Model Management
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Prediction */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-yellow-600" />
                Prediction & Inference
              </CardTitle>
              <CardDescription>Run predictions on images and videos</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Link href="/predict/image">
                  <Button className="w-full justify-start bg-yellow-600 hover:bg-yellow-700">
                    <Camera className="h-4 w-4 mr-2" />
                    Image Prediction
                  </Button>
                </Link>
                <Link href="/predict/video">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    <Video className="h-4 w-4 mr-2" />
                    Video Prediction
                  </Button>
                </Link>
                <Link href="/predict/batch">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    <Upload className="h-4 w-4 mr-2" />
                    Batch Processing
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Latest workflow actions and system events</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { action: "Training started", dataset: "construction_v2", time: "2 minutes ago", status: "running" },
                { action: "Images collected", count: "247 images", time: "15 minutes ago", status: "completed" },
                { action: "Prediction completed", model: "yolov8n_custom", time: "1 hour ago", status: "completed" },
                { action: "Dataset organized", dataset: "vehicles_dataset", time: "2 hours ago", status: "completed" },
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-2 h-2 rounded-full ${
                        item.status === "running" ? "bg-green-500 animate-pulse" : "bg-gray-400"
                      }`}
                    />
                    <div>
                      <p className="font-medium">{item.action}</p>
                      <p className="text-sm text-muted-foreground">{item.dataset || item.count || item.model}</p>
                    </div>
                  </div>
                  <span className="text-sm text-muted-foreground">{item.time}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
