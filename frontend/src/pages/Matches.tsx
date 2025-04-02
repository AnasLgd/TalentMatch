
import React, { useState } from "react";
import { Search, Filter, ChevronDown, BarChart3, ListFilter, UserCheck, Briefcase } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface Match {
  id: number;
  consultant: {
    name: string;
    role: string;
    skills: string[];
    status: "Disponible" | "En mission" | "Congés" | "Formation";
  };
  tender: {
    title: string;
    client: string;
    requiredSkills: string[];
    status: "Nouveau" | "En cours" | "En attente" | "Fermé";
  };
  matchScore: number;
  matchStatus: "Proposé" | "En discussion" | "Accepté" | "Refusé";
}

const matches: Match[] = [
  {
    id: 1,
    consultant: { name: "Sophie Martin", role: "Développeur Frontend", skills: ["React", "TypeScript", "Tailwind"], status: "Disponible" },
    tender: { title: "Développeur React/Node", client: "Société ABC", requiredSkills: ["React", "Node.js", "MongoDB"], status: "Nouveau" },
    matchScore: 85,
    matchStatus: "Proposé"
  },
  {
    id: 2,
    consultant: { name: "Thomas Bernard", role: "Data Scientist", skills: ["Python", "TensorFlow", "SQL"], status: "En mission" },
    tender: { title: "Data Engineer", client: "Société MNO", requiredSkills: ["Spark", "Hadoop", "Python"], status: "En attente" },
    matchScore: 72,
    matchStatus: "En discussion"
  },
  {
    id: 3,
    consultant: { name: "Emma Laurent", role: "UX Designer", skills: ["Figma", "Adobe XD", "Sketch"], status: "Disponible" },
    tender: { title: "UX/UI Designer", client: "Entreprise PQR", requiredSkills: ["Figma", "Sketch", "Adobe XD"], status: "En cours" },
    matchScore: 95,
    matchStatus: "Accepté"
  },
  {
    id: 4,
    consultant: { name: "Lucas Dubois", role: "DevOps Engineer", skills: ["Docker", "Kubernetes", "AWS"], status: "En mission" },
    tender: { title: "DevOps Engineer", client: "Groupe STU", requiredSkills: ["Docker", "Kubernetes", "CI/CD"], status: "En attente" },
    matchScore: 88,
    matchStatus: "En discussion"
  },
];

const getConsultantStatusColor = (status: Match["consultant"]["status"]) => {
  switch (status) {
    case "Disponible":
      return "bg-green-500/20 text-green-500";
    case "En mission":
      return "bg-blue-500/20 text-blue-500";
    case "Congés":
      return "bg-amber-500/20 text-amber-500";
    case "Formation":
      return "bg-purple-500/20 text-purple-500";
    default:
      return "bg-gray-500/20 text-gray-500";
  }
};

const getTenderStatusColor = (status: Match["tender"]["status"]) => {
  switch (status) {
    case "Nouveau":
      return "bg-blue-500/20 text-blue-500";
    case "En cours":
      return "bg-green-500/20 text-green-500";
    case "En attente":
      return "bg-amber-500/20 text-amber-500";
    case "Fermé":
      return "bg-red-500/20 text-red-500";
    default:
      return "bg-gray-500/20 text-gray-500";
  }
};

const getMatchStatusColor = (status: Match["matchStatus"]) => {
  switch (status) {
    case "Proposé":
      return "bg-blue-500/20 text-blue-500 border-blue-500";
    case "En discussion":
      return "bg-amber-500/20 text-amber-500 border-amber-500";
    case "Accepté":
      return "bg-green-500/20 text-green-500 border-green-500";
    case "Refusé":
      return "bg-red-500/20 text-red-500 border-red-500";
    default:
      return "bg-gray-500/20 text-gray-500 border-gray-500";
  }
};

const getMatchScoreColor = (score: number) => {
  if (score >= 90) return "bg-green-500";
  if (score >= 75) return "bg-blue-500";
  if (score >= 60) return "bg-amber-500";
  return "bg-red-500";
};

const Matches = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [activeTab, setActiveTab] = useState("all");
  const [filteredMatches, setFilteredMatches] = useState(matches);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    
    let filtered = [...matches];
    
    // Filtrer par terme de recherche
    if (term.trim() !== "") {
      filtered = filtered.filter(
        (match) =>
          match.consultant.name.toLowerCase().includes(term) ||
          match.tender.title.toLowerCase().includes(term) ||
          match.tender.client.toLowerCase().includes(term)
      );
    }
    
    // Filtrer par statut de matching
    if (activeTab !== "all") {
      filtered = filtered.filter((match) => match.matchStatus.toLowerCase() === activeTab);
    }
    
    setFilteredMatches(filtered);
  };

  const handleTabChange = (value: string) => {
    setActiveTab(value);
    
    let filtered = [...matches];
    
    // Filtrer par terme de recherche
    if (searchTerm.trim() !== "") {
      filtered = filtered.filter(
        (match) =>
          match.consultant.name.toLowerCase().includes(searchTerm) ||
          match.tender.title.toLowerCase().includes(searchTerm) ||
          match.tender.client.toLowerCase().includes(searchTerm)
      );
    }
    
    // Filtrer par statut de matching
    if (value !== "all") {
      filtered = filtered.filter((match) => match.matchStatus.toLowerCase() === value);
    }
    
    setFilteredMatches(filtered);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Matching</h1>
        <p className="text-muted-foreground">
          Trouvez les meilleures correspondances entre consultants et appels d'offres.
        </p>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative max-w-md w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Rechercher par consultant, offre..."
            className="pl-10"
            value={searchTerm}
            onChange={handleSearch}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline">
            <Filter className="mr-2 h-4 w-4" />
            Filtres avancés
            <ChevronDown className="ml-2 h-4 w-4" />
          </Button>
          <Button>
            <BarChart3 className="mr-2 h-4 w-4" />
            Matching automatique
          </Button>
        </div>
      </div>

      <div className="space-y-6">
        <Tabs defaultValue="all" value={activeTab} onValueChange={handleTabChange}>
          <TabsList className="grid w-full grid-cols-4 mb-4">
            <TabsTrigger value="all">Tous</TabsTrigger>
            <TabsTrigger value="proposé">Proposés</TabsTrigger>
            <TabsTrigger value="en discussion">En discussion</TabsTrigger>
            <TabsTrigger value="accepté">Acceptés</TabsTrigger>
          </TabsList>
          
          <TabsContent value="all" className="mt-0">
            <div className="grid gap-4 md:grid-cols-2">
              {filteredMatches.map((match) => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </TabsContent>
          
          <TabsContent value="proposé" className="mt-0">
            <div className="grid gap-4 md:grid-cols-2">
              {filteredMatches.map((match) => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </TabsContent>
          
          <TabsContent value="en discussion" className="mt-0">
            <div className="grid gap-4 md:grid-cols-2">
              {filteredMatches.map((match) => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </TabsContent>
          
          <TabsContent value="accepté" className="mt-0">
            <div className="grid gap-4 md:grid-cols-2">
              {filteredMatches.map((match) => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

interface MatchCardProps {
  match: Match;
}

const MatchCard: React.FC<MatchCardProps> = ({ match }) => {
  return (
    <Card className="border-border/40">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-center">
          <div className="space-y-1">
            <CardTitle className="flex items-center gap-2">
              <span className={`inline-flex h-2 w-2 rounded-full ${
                match.consultant.status === "Disponible" ? "bg-green-500" : "bg-amber-500"
              }`}></span>
              {match.consultant.name}
            </CardTitle>
            <CardDescription>{match.consultant.role}</CardDescription>
          </div>
          <span className={`border px-3 py-1 rounded-full text-xs font-medium ${getMatchStatusColor(match.matchStatus)}`}>
            {match.matchStatus}
          </span>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <div className="text-sm font-medium text-muted-foreground flex items-center">
              <Briefcase className="h-4 w-4 mr-1" /> {match.tender.title}
            </div>
            <div className="text-sm text-muted-foreground">
              {match.tender.client}
            </div>
          </div>
        </div>
        
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="flex items-center text-muted-foreground">
              <ListFilter className="h-4 w-4 mr-1" /> 
              Score de correspondance
            </span>
            <span className="font-medium">{match.matchScore}%</span>
          </div>
          <Progress value={match.matchScore} className="h-2" indicatorClassName={getMatchScoreColor(match.matchScore)} />
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-sm font-medium mb-2 flex items-center">
              <UserCheck className="h-4 w-4 mr-1" />
              <span>Compétences</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {match.consultant.skills.map((skill, idx) => (
                <Badge key={idx} variant="secondary">{skill}</Badge>
              ))}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium mb-2 flex items-center">
              <Briefcase className="h-4 w-4 mr-1" />
              <span>Requises</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {match.tender.requiredSkills.map((skill, idx) => (
                <Badge key={idx} variant="secondary">{skill}</Badge>
              ))}
            </div>
          </div>
        </div>
        
        <div className="flex gap-2 pt-2">
          <Button variant="outline" className="w-full">Détails</Button>
          <Button className="w-full">Contacter</Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default Matches;
