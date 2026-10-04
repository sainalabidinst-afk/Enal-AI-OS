# Vision Engine

## Responsibility
Provide real-time computer vision inference for visual perception use cases.

## Components
- `VisionEngine`
- `ModelLoader`
- `InferencePipeline`
- `DetectionFormatter`

## Models
- YOLO for object detection.
- OpenCV for preprocessing and postprocessing.
- TensorRT for Jetson Nano optimization.

## Use Cases
- Mining/HSE: PPE detection, structural crack analysis.
- Smart Agriculture: livestock monitoring, thermal analysis.
- Manufacturing: defect detection, quality control.

## Data Contract
```json
{
  "inference_id": "string",
  "model": "string",
  "latency_ms": 0,
  "detections": [
    {
      "label": "string",
      "confidence": 0.0,
      "bbox": [0, 0, 0, 0]
    }
  ]
}
```

## VS Code Deliverables
- Add `apps/vision/vision_engine.py`
- Add `apps/vision/inference_pipeline.py`
- Add backend endpoint `/api/v1/vision/infer`.
