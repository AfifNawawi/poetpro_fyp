import 'package:flutter/material.dart';
import '../services/api_services.dart';
import '../utils/pdf_generator.dart';
import 'package:printing/printing.dart';

class AnalyzerPage extends StatefulWidget {
  final String poemType;

  const AnalyzerPage({super.key, required this.poemType});

  @override
  State<AnalyzerPage> createState() => _AnalyzerPageState();
}

class _AnalyzerPageState extends State<AnalyzerPage> {
  final TextEditingController _poemController = TextEditingController();

  int? lineCount;
  String? structure;
  String? rhymePattern;
  String? message;
  String? suggestion; // ✅ NEW (LLM output)
  bool isLoading = false;

  Future<void> analyzePoem() async {
    if (_poemController.text.trim().isEmpty) return;

    setState(() {
      isLoading = true;
      lineCount = null;
      structure = null;
      rhymePattern = null;
      message = null;
      suggestion = null;
    });

    final response = await ApiService.analyze(
      _poemController.text,
      widget.poemType,
    );

    setState(() {
      lineCount = response['line_count'];
      structure = response['structure'];
      rhymePattern = response['rhyme_pattern'];
      message = response['message'] ?? response['error'];
      suggestion = response['ai_suggestion']; // 👈 LLM result
      isLoading = false;
    });
  }

  Future<void> exportToPdf() async {
    final file = await PdfGenerator.generatePoemReport(
      poem: _poemController.text,
      feedback:
          '''
Line Count: $lineCount
Structure: $structure
Rhyme Pattern: $rhymePattern

Rule-based Analysis:
$message

AI Suggestion:
${suggestion ?? "No suggestion generated."}
''',
    );

    await Printing.layoutPdf(onLayout: (format) async => file.readAsBytes());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PoetPro ${widget.poemType.toUpperCase()} Analyzer'),
        backgroundColor: Colors.green,
      ),
      backgroundColor: Colors.green[100],
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            /// Input box
            TextField(
              controller: _poemController,
              maxLines: 6,
              decoration: InputDecoration(
                hintText: 'Type or paste your ${widget.poemType} here',
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),

            const SizedBox(height: 15),

            /// Analyze button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: analyzePoem,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.lightGreenAccent,
                  foregroundColor: Colors.black,
                ),
                child: const Text('Analyze'),
              ),
            ),

            const SizedBox(height: 20),

            if (isLoading) const CircularProgressIndicator(),

            if (!isLoading && message != null)
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      /// Rule-based result
                      const Text(
                        'Analysis Result',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      const SizedBox(height: 10),

                      Card(
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Line Count: $lineCount'),
                              Text('Structure: $structure'),
                              Text('Rhyme Pattern: $rhymePattern'),
                              const SizedBox(height: 8),
                              Text(message ?? ''),
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(height: 20),

                      /// 🔥 AI Suggestion section
                      const Text(
                        'AI Suggestion',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      const SizedBox(height: 10),

                      Card(
                        color: Colors.lightGreen[50],
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Text(
                            suggestion ??
                                'No AI suggestion available for this input.',
                            style: const TextStyle(fontSize: 15),
                          ),
                        ),
                      ),

                      const SizedBox(height: 16),

                      /// Export PDF
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          icon: const Icon(Icons.picture_as_pdf),
                          label: const Text('Export PDF'),
                          onPressed: exportToPdf,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
