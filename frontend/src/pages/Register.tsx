
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Eye, EyeOff, Lock, Mail, User, Building } from "lucide-react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import LogoSection from "@/components/common/LogoSection";

const Register = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    companyName: "",
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Registration data:", formData);
    // Ici nous ajouterons la logique d'inscription
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <LogoSection className="mb-8" />
        
        <Card className="border-border/40 bg-card/70 backdrop-blur-md">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl font-bold text-center">Créer un compte</CardTitle>
            <CardDescription className="text-center text-muted-foreground">
              Inscrivez-vous pour accéder à la plateforme TalentMatch
            </CardDescription>
          </CardHeader>
          
          <form onSubmit={handleRegister}>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="relative">
                  <User className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
                  <Input
                    name="firstName"
                    placeholder="Prénom"
                    className="pl-10"
                    value={formData.firstName}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="relative">
                  <Input
                    name="lastName"
                    placeholder="Nom"
                    value={formData.lastName}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="relative">
                <Building className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
                <Input
                  name="companyName"
                  placeholder="Nom de votre entreprise"
                  className="pl-10"
                  value={formData.companyName}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="relative">
                <Mail className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
                <Input
                  type="email"
                  name="email"
                  placeholder="Email professionnel"
                  className="pl-10"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div className="relative">
                <Lock className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
                <Input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Mot de passe"
                  className="pl-10 pr-10"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-muted-foreground hover:text-foreground"
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5" />
                  ) : (
                    <Eye className="h-5 w-5" />
                  )}
                </button>
              </div>
              
              <div className="text-xs text-muted-foreground">
                En créant un compte, vous acceptez nos{" "}
                <Link to="/terms" className="text-primary hover:underline">
                  Conditions d'utilisation
                </Link>{" "}
                et notre{" "}
                <Link to="/privacy" className="text-primary hover:underline">
                  Politique de confidentialité
                </Link>
                .
              </div>
              
              <Button type="submit" className="w-full">
                S'inscrire
              </Button>
              
              <div className="flex items-center space-x-2">
                <Separator className="flex-1" />
                <span className="text-xs text-muted-foreground">OU</span>
                <Separator className="flex-1" />
              </div>
              
              <Button variant="outline" className="w-full">
                <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
                  <path
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                    fill="#4285F4"
                  />
                  <path
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                    fill="#34A853"
                  />
                  <path
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                    fill="#FBBC05"
                  />
                  <path
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                    fill="#EA4335"
                  />
                </svg>
                Continuer avec Google
              </Button>
            </CardContent>
          </form>
          
          <CardFooter>
            <div className="text-center w-full text-sm">
              Vous avez déjà un compte?{" "}
              <Link to="/login" className="text-primary hover:underline">
                Connectez-vous
              </Link>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default Register;
