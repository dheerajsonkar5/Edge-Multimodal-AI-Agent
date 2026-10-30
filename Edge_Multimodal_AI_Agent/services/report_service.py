"""
Report Service - Generate Reports and Save Snapshots
"""
import os
import json
import csv
import cv2
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from core.logger import get_logger
from core.config import settings

logger = get_logger()


class ReportService:
    """Handle report generation and management"""
    
    def __init__(self):
        self.reports_dir = Path(settings.REPORTS_DIR) if hasattr(settings, 'REPORTS_DIR') else Path("reports")
        self.snapshots_dir = Path(settings.SNAPSHOTS_DIR) if hasattr(settings, 'SNAPSHOTS_DIR') else Path("snapshots")
        
        # Create directories
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        
        self.report_counter = 0
        logger.info(f"✅ ReportService initialized: Reports: {self.reports_dir}, Snapshots: {self.snapshots_dir}")
    
    def generate(self, events: Optional[List[Dict]] = None, format: str = "json") -> str:
        """
        Generate a report
        
        Args:
            events: List of events (if None, generates sample report)
            format: json or csv
            
        Returns:
            Path to generated report
        """
        try:
            # ✅ FIXED: Log events count
            if events is None:
                events = []
                logger.info("📊 No events provided, generating empty report")
            else:
                logger.info(f"📊 Generating report with {len(events)} events")
            
            # ✅ FIXED: Create report with proper event data
            report = {
                "id": f"REP_{int(datetime.now().timestamp())}_{self.report_counter}",
                "timestamp": datetime.now().isoformat(),
                "total_events": len(events),
                "events": events,
                "summary": self._generate_summary(events),
                "statistics": self._get_statistics()
            }
            
            self.report_counter += 1
            
            # Save report
            if format == "json":
                filename = self.reports_dir / f"report_{report['id']}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                logger.info(f"✅ JSON report saved: {filename}")
                
            elif format == "csv":
                filename = self.reports_dir / f"report_{report['id']}.csv"
                self._save_csv(report, filename)
                logger.info(f"✅ CSV report saved: {filename}")
                
            else:
                filename = self.reports_dir / f"report_{report['id']}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                logger.info(f"✅ JSON report saved: {filename}")
            
            return str(filename)
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {str(e)}")
            # Return a fallback report path
            fallback_path = self.reports_dir / f"report_fallback_{int(datetime.now().timestamp())}.json"
            with open(fallback_path, 'w') as f:
                json.dump({"error": str(e), "timestamp": datetime.now().isoformat()}, f)
            return str(fallback_path)
    
    def _get_sample_events(self) -> List[Dict]:
        """Generate sample events for testing"""
        return [
            {
                "id": "EVT_001",
                "timestamp": datetime.now().isoformat(),
                "type": "fatigue",
                "severity": "high",
                "description": "Fatigue detected: 75.5%"
            },
            {
                "id": "EVT_002",
                "timestamp": datetime.now().isoformat(),
                "type": "multiple_persons",
                "severity": "medium",
                "description": "2 persons detected in workspace"
            }
        ]
    
    def _generate_summary(self, events: List[Dict]) -> Dict:
        """Generate summary from events"""
        summary = {
            "total": len(events),
            "by_type": {},
            "by_severity": {},
            "time_range": None
        }
        
        if events:
            # By type
            for event in events:
                etype = event.get("type", event.get("event_type", "unknown"))
                summary["by_type"][etype] = summary["by_type"].get(etype, 0) + 1
            
            # By severity
            for event in events:
                sev = event.get("severity", "info")
                summary["by_severity"][sev] = summary["by_severity"].get(sev, 0) + 1
            
            # Time range
            times = [e.get("timestamp") for e in events if e.get("timestamp")]
            if times:
                summary["time_range"] = {
                    "start": min(times),
                    "end": max(times)
                }
        
        return summary
    
    def _get_statistics(self) -> Dict:
        """Get system statistics"""
        return {
            "total_reports": self.report_counter,
            "reports_dir": str(self.reports_dir),
            "snapshots_dir": str(self.snapshots_dir),
            "timestamp": datetime.now().isoformat()
        }
    
    def _save_csv(self, report: Dict, filename: Path):
        """Save report as CSV"""
        try:
            if report.get("events"):
                # Get all unique keys from events
                keys = set()
                for event in report["events"]:
                    keys.update(event.keys())
                keys = list(keys)
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(report["events"])
                logger.info(f"✅ CSV saved: {filename}")
        except Exception as e:
            logger.error(f"❌ CSV save failed: {str(e)}")
    
    def save_snapshot(self, frame) -> str:
        """
        Save a snapshot image
        
        Args:
            frame: Image frame (numpy array)
            
        Returns:
            Path to saved snapshot
        """
        try:
            if frame is None:
                logger.warning("Frame is None, cannot save snapshot")
                return ""
            
            filename = f"snapshot_{int(datetime.now().timestamp())}.jpg"
            filepath = self.snapshots_dir / filename
            cv2.imwrite(str(filepath), frame)
            
            logger.info(f"✅ Snapshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Snapshot save failed: {str(e)}")
            return ""
    
    def total_reports(self) -> int:
        """Get total number of reports"""
        try:
            return len(list(self.reports_dir.glob("report_*.json")))
        except:
            return self.report_counter
    
    def list_reports(self) -> List[Dict]:
        """List all reports with metadata"""
        reports = []
        try:
            for file in sorted(self.reports_dir.glob("report_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        reports.append({
                            "id": data.get("id", file.stem),
                            "filename": file.name,
                            "timestamp": data.get("timestamp", ""),
                            "total_events": data.get("total_events", 0),
                            "path": str(file)
                        })
                except Exception as e:
                    logger.warning(f"Could not read report {file}: {e}")
                    reports.append({
                        "id": file.stem,
                        "filename": file.name,
                        "timestamp": "",
                        "total_events": 0,
                        "path": str(file)
                    })
        except Exception as e:
            logger.error(f"❌ List reports failed: {str(e)}")
        
        return reports
    
    def get_report(self, report_id: str) -> Optional[Dict]:
        """Get a specific report by ID"""
        try:
            # Try JSON first
            json_path = self.reports_dir / f"report_{report_id}.json"
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Try with different patterns
            for file in self.reports_dir.glob(f"*{report_id}*.json"):
                if file.exists():
                    with open(file, 'r', encoding='utf-8') as f:
                        return json.load(f)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Get report failed: {str(e)}")
            return None
    
    def delete_report(self, report_id: str) -> bool:
        """Delete a report by ID"""
        try:
            deleted = False
            for file in self.reports_dir.glob(f"*{report_id}*.json"):
                file.unlink()
                deleted = True
                logger.info(f"✅ Deleted report: {file}")
            
            # Also delete CSV if exists
            for file in self.reports_dir.glob(f"*{report_id}*.csv"):
                file.unlink()
                deleted = True
            
            return deleted
            
        except Exception as e:
            logger.error(f"❌ Delete report failed: {str(e)}")
            return False