
import React from "react";
import { BarChart3, Users, Briefcase, Search, ArrowUpRight } from "lucide-react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const Dashboard = () => {
  const statCards = [
    {
      title: "Consultants",
      value: "128",
      change: "+12%",
      positive: true,
      description: "vs. mois précédent",
      icon: Users,
      color: "bg-blue-500/20 text-blue-500",
    },
    {
      title: "Appels d'offres",
      value: "45",
      change: "+7%",
      positive: true,
      description: "vs. mois précédent",
      icon: Briefcase,
      color: "bg-green-500/20 text-green-500",
    },
    {
      title: "Taux de matching",
      value: "74%",
      change: "-3%",
      positive: false,
      description: "vs. mois précédent",
      icon: Search,
      color: "bg-purple-500/20 text-purple-500",
    },
    {
      title: "Consultants disponibles",
      value: "23",
      change: "+5%",
      positive: true,
      description: "vs. mois précédent",
      icon: BarChart3,
      color: "bg-amber-500/20 text-amber-500",
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Tableau de bord</h1>
        <p className="text-muted-foreground">
          Bienvenue sur votre tableau de bord, découvrez vos statistiques et activités récentes.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => (
          <Card key={card.title} className="stats-card card-hover-effect">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
              <div className={`icon-container ${card.color}`}>
                <card.icon className="h-4 w-4" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{card.value}</div>
              <div className="text-xs flex items-center pt-1">
                <span className={card.positive ? "text-primary" : "text-red-500"}>
                  {card.change}
                </span>
                <span className="text-muted-foreground ml-1">{card.description}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-6">
        <Card className="dashboard-card card-hover-effect md:col-span-4">
          <CardHeader>
            <CardTitle>Activité des appels d'offres</CardTitle>
            <CardDescription>
              Distribution des appels d'offres par statut
            </CardDescription>
          </CardHeader>
          <CardContent className="py-2">
            <div className="h-[220px] flex items-end gap-2">
              {/* Graphique amélioré */}
              <div className="relative flex flex-col items-center w-full h-full">
                <div className="flex justify-around w-full absolute bottom-0">
                  {['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'].map((day, index) => {
                    // Générer des hauteurs aléatoires qui correspondent mieux à l'image
                    const heights = [65, 45, 80, 55, 90, 35, 20];
                    const height = heights[index];
                    
                    return (
                      <div key={day} className="flex flex-col items-center group">
                        <div className="h-[140px] w-10 bg-secondary/20 rounded-t-md flex items-end transition-all duration-300 overflow-hidden">
                          <div
                            className="w-full bg-primary rounded-t-md transition-all duration-500 ease-out"
                            style={{ height: `${height}%` }}
                          ></div>
                        </div>
                        <div className="mt-2 text-xs text-muted-foreground relative">
                          <span>{day}</span>
                          <div className="absolute -top-7 left-1/2 transform -translate-x-1/2 bg-primary text-primary-foreground px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                            {height}%
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="dashboard-card card-hover-effect md:col-span-3">
          <CardHeader>
            <CardTitle>Statuts des appels d'offres</CardTitle>
            <CardDescription>
              Distribution actuelle par état
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm mt-2">
                  <div className="flex items-center">
                    <div className="h-3 w-3 rounded-full bg-primary mr-2"></div>
                    <span className="text-muted-foreground">En cours</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>24</span>
                    <span className="text-muted-foreground text-xs">(53%)</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div className="progress-bar-fill" style={{ width: '53%' }}></div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center">
                    <div className="h-3 w-3 rounded-full bg-blue-500 mr-2"></div>
                    <span className="text-muted-foreground">Nouveaux</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>12</span>
                    <span className="text-muted-foreground text-xs">(27%)</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div className="progress-bar-fill" style={{ width: '27%', backgroundColor: 'hsl(210, 100%, 50%)' }}></div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center">
                    <div className="h-3 w-3 rounded-full bg-amber-500 mr-2"></div>
                    <span className="text-muted-foreground">En attente</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>6</span>
                    <span className="text-muted-foreground text-xs">(13%)</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div className="progress-bar-fill" style={{ width: '13%', backgroundColor: 'hsl(45, 100%, 50%)' }}></div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center">
                    <div className="h-3 w-3 rounded-full bg-red-500 mr-2"></div>
                    <span className="text-muted-foreground">Fermés</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>3</span>
                    <span className="text-muted-foreground text-xs">(7%)</span>
                  </div>
                </div>
                <div className="progress-bar">
                  <div className="progress-bar-fill" style={{ width: '7%', backgroundColor: 'hsl(0, 100%, 50%)' }}></div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="dashboard-card card-hover-effect">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Derniers consultants</CardTitle>
              <CardDescription className="text-muted-foreground">
                Consultants récemment ajoutés à la plateforme
              </CardDescription>
            </div>
            <a href="/consultants" className="flex items-center text-sm text-primary hover:underline transition-colors">
              Voir tout <ArrowUpRight className="ml-1 h-4 w-4" />
            </a>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: "Sophie Martin", role: "Développeur Frontend", skills: ["React", "TypeScript", "Tailwind"], available: true },
                { name: "Thomas Bernard", role: "Data Scientist", skills: ["Python", "TensorFlow", "SQL"], available: false },
                { name: "Emma Laurent", role: "UX Designer", skills: ["Figma", "Adobe XD", "Sketch"], available: true },
                { name: "Lucas Dubois", role: "DevOps Engineer", skills: ["Docker", "Kubernetes", "AWS"], available: false },
              ].map((consultant, index) => (
                <div key={index} className="flex items-center justify-between py-2">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-full bg-secondary/20 flex items-center justify-center">
                      <span className="font-medium text-sm">{consultant.name.split(' ').map(n => n[0]).join('')}</span>
                    </div>
                    <div>
                      <p className="font-medium">{consultant.name}</p>
                      <p className="text-sm text-muted-foreground">{consultant.role}</p>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <span className={`status-badge ${
                      consultant.available
                        ? "status-badge-active"
                        : "status-badge-pending"
                    }`}>
                      {consultant.available ? "Disponible" : "En mission"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="dashboard-card card-hover-effect">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Derniers appels d'offres</CardTitle>
              <CardDescription className="text-muted-foreground">
                Appels d'offres récemment publiés
              </CardDescription>
            </div>
            <a href="/tenders" className="flex items-center text-sm text-primary hover:underline transition-colors">
              Voir tout <ArrowUpRight className="ml-1 h-4 w-4" />
            </a>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { title: "Développeur React/Node", client: "Société ABC", skills: ["React", "Node.js", "MongoDB"], status: "Nouveau" },
                { title: "Scrum Master", client: "Entreprise XYZ", skills: ["Agile", "Jira", "Scrum"], status: "En cours" },
                { title: "Architecte Cloud", client: "Groupe DEF", skills: ["AWS", "Azure", "Terraform"], status: "En cours" },
                { title: "Data Engineer", client: "Société MNO", skills: ["Spark", "Hadoop", "Python"], status: "En attente" },
              ].map((tender, index) => (
                <div key={index} className="flex items-center justify-between py-2">
                  <div>
                    <p className="font-medium">{tender.title}</p>
                    <p className="text-sm text-muted-foreground">{tender.client}</p>
                  </div>
                  <div className="flex items-center">
                    <span className={`status-badge ${
                      tender.status === "Nouveau"
                        ? "status-badge-new"
                        : tender.status === "En cours"
                        ? "status-badge-active"
                        : "status-badge-pending"
                    }`}>
                      {tender.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
