import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Store Opening AI application', () => {
  render(<App />);
  // The app should render the login page initially when not authenticated
  const appElement = screen.getByText(/Store Opening AI/i);
  expect(appElement).toBeInTheDocument();
});
