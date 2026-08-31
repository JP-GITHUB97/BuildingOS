import 'package:flutter_test/flutter_test.dart';

import 'package:buildingos_app/main.dart';

void main() {
  testWidgets('BuildingOS démarre correctement', (WidgetTester tester) async {
    await tester.pumpWidget(const BuildingOSApp());

    expect(find.text('BuildingOS'), findsOneWidget);
    expect(find.text('Bienvenue dans BuildingOS'), findsOneWidget);
  });
}