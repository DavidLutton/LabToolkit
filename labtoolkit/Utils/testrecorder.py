class TestRecorder:
    
    def __init__(self, dest):
        self.dest = dest
        
    def __enter__(self):
        writer = pd.ExcelWriter(self.dest, engine='openpyxl')
        if dest.exists():
            writer.book = load_workbook(self.dest)
        self.writer = writer
        return self
        
    def __exit__(self, a, b, c):
        try:
            if len(self.writer.book.sheetnames) > 0:
                # Check at least one sheet has been written before attempting to save
                self.writer.save()
        except PermissionError as e:
            print(f'{self.dest.stem} spreadsheet is open in another application')
        finally:
            pass
        
    def save_results(self, data, sheet_name):
        data.to_excel(self.writer, sheet_name=sheet_name, index=False)
        # 
        self.writer.save()
        