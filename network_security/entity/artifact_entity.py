from dataclasses import dataclass

@dataclass
class DataIngestArtifact:
    trained_file_path: str
    test_file_path: str