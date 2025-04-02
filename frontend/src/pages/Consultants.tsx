
import React, { useState } from "react";
import { 
  Search, 
  Plus, 
  Filter, 
  ArrowUpDown, 
  MoreVertical, 
  Edit, 
  Trash2, 
  FileText,
  Download 
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

interface Consultant {
  id: number;
  name: string;
  role: string;
  experience: string;
  skills: string[];
  status: "Disponible" | "En mission" | "Congés" | "Formation";
}

const consultants: Consultant[] = [
  { id: 1, name: "Sophie Martin", role: "Développeur Frontend", experience: "5 ans", skills: ["React", "TypeScript", "Tailwind"], status: "Disponible" },
  { id: 2, name: "Thomas Bernard", role: "Data Scientist", experience: "4 ans", skills: ["Python", "TensorFlow", "SQL"], status: "En mission" },
  { id: 3, name: "Emma Laurent", role: "UX Designer", experience: "6 ans", skills: ["Figma", "Adobe XD", "Sketch"], status: "Disponible" },
  { id: 4, name: "Lucas Dubois", role: "DevOps Engineer", experience: "7 ans", skills: ["Docker", "Kubernetes", "AWS"], status: "En mission" },
  { id: 5, name: "Chloé Petit", role: "Développeur Backend", experience: "3 ans", skills: ["Java", "Spring", "PostgreSQL"], status: "Formation" },
  { id: 6, name: "Maxime Leroy", role: "Chef de projet", experience: "8 ans", skills: ["Agile", "JIRA", "MS Project"], status: "Disponible" },
  { id: 7, name: "Léa Fontaine", role: "Analyste Business", experience: "4 ans", skills: ["Power BI", "Excel", "SQL"], status: "En mission" },
  { id: 8, name: "Hugo Martin", role: "Développeur Mobile", experience: "5 ans", skills: ["Swift", "Kotlin", "Flutter"], status: "Congés" },
];

const getStatusColor = (status: Consultant["status"]) => {
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

const Consultants = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredConsultants, setFilteredConsultants] = useState(consultants);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    
    if (term.trim() === "") {
      setFilteredConsultants(consultants);
    } else {
      const filtered = consultants.filter(
        (consultant) =>
          consultant.name.toLowerCase().includes(term) ||
          consultant.role.toLowerCase().includes(term) ||
          consultant.skills.some((skill) => skill.toLowerCase().includes(term))
      );
      setFilteredConsultants(filtered);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Consultants</h1>
        <p className="text-muted-foreground">
          Gérez vos consultants, leurs compétences et disponibilités.
        </p>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative max-w-md w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Rechercher par nom, compétence..."
            className="pl-10"
            value={searchTerm}
            onChange={handleSearch}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Ajouter un consultant
          </Button>
        </div>
      </div>

      <Card className="border-border/40">
        <div className="relative w-full overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[300px]">
                  <div className="flex items-center">
                    Nom
                    <ArrowUpDown className="ml-1 h-3 w-3" />
                  </div>
                </TableHead>
                <TableHead>
                  <div className="flex items-center">
                    Rôle
                    <ArrowUpDown className="ml-1 h-3 w-3" />
                  </div>
                </TableHead>
                <TableHead>Expérience</TableHead>
                <TableHead>Compétences</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredConsultants.map((consultant) => (
                <TableRow key={consultant.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
                        <span className="text-xs">
                          {consultant.name.split(" ").map(n => n[0]).join("")}
                        </span>
                      </div>
                      <span>{consultant.name}</span>
                    </div>
                  </TableCell>
                  <TableCell>{consultant.role}</TableCell>
                  <TableCell>{consultant.experience}</TableCell>
                  <TableCell>
                    <div className="flex flex-wrap gap-1">
                      {consultant.skills.map((skill, idx) => (
                        <Badge key={idx} variant="secondary">{skill}</Badge>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className={`inline-flex rounded-full px-2 py-1 text-xs ${getStatusColor(consultant.status)}`}>
                      {consultant.status}
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon">
                          <MoreVertical className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem>
                          <FileText className="mr-2 h-4 w-4" />
                          <span>Voir profil</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Edit className="mr-2 h-4 w-4" />
                          <span>Modifier</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Download className="mr-2 h-4 w-4" />
                          <span>Exporter CV</span>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="text-red-500">
                          <Trash2 className="mr-2 h-4 w-4" />
                          <span>Supprimer</span>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </Card>
    </div>
  );
};

export default Consultants;
