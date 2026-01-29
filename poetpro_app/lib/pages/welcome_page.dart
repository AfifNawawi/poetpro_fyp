import 'package:flutter/material.dart';
import 'pantun_analyzer_page.dart';
import 'syair_analyzer_page.dart';

class WelcomePage extends StatelessWidget {
  const WelcomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1FAF38),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Image.asset(
                'assets/poetpro_logo.png',
                height: 300,
              ),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: () => _choosePoemType(context),
                child: const Text('Start Checking'),
              ),
              const SizedBox(height: 10),
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Quit'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

void _choosePoemType(BuildContext context) {
  showDialog(
    context: context,
    builder: (_) => AlertDialog(
      title: const Text('Choose Poem Type'),
      actions: [
        TextButton(
          onPressed: () {
            Navigator.pop(context);
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const PantunAnalyzerPage()),
            );
          },
          child: const Text('Pantun'),
        ),
        TextButton(
          onPressed: () {
            Navigator.pop(context);
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SyairAnalyzerPage()),
            );
          },
          child: const Text('Syair'),
        ),
      ],
    ),
  );
}



