import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  template: `
    <header>
      <h1>Generated Admin</h1>
    </header>
    <main>
      <p>Экраны генерируются агентом 06 из ui-spec.json.</p>
    </main>
  `,
  styles: [`
    header { padding: 1rem; background: #1976d2; color: #fff; }
    main { padding: 1rem; }
  `],
})
export class HomeComponent {}
